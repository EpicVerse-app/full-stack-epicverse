from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import io
import uuid
import json

# Local modules
from app.services.speech_to_text import transcribe_audio
from app.services.ai_pipeline import run_ai_pipeline
from app.services.text_to_speech import synthesize_speech
from app.services.storage import upload_to_gcs, log_interaction
from app.services.user_db import save_user, UserRecord, get_user
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/sync-user")
async def sync_user(user: UserRecord):
    """Saves user info to the SQL database."""
    await save_user(user)
    return {"status": "success", "message": "User synchronized"}

@router.get("/user/{firebase_id}")
async def fetch_user(firebase_id: str):
    """Fetches user info from the SQL database."""
    user = await get_user(firebase_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.websocket("/ws-audio")
async def websocket_audio(websocket: WebSocket, gameMode: str = "Mode 1", sessionId: str = "default"):
    """Live streaming endpoint to receive audio chunks and process instantly."""
    await websocket.accept()
    print(f"\n[WS] New Connection - Mode: {gameMode}, Session: {sessionId}", flush=True)
    # Send an initial message to let the client know we are ready
    await websocket.send_text(json.dumps({"status": "Connected", "message": "Established connection to EpicVerse AI."}))
    audio_bytes = bytearray()
    
    try:
        while True:
            # We can receive either binary audio chunks or JSON text commands
            message = await websocket.receive()
            
            if message.get("type") == "websocket.disconnect":
                print(f"[WS] Client disconnected ({sessionId})", flush=True)
                break
                
            if "bytes" in message:
                # print(f"DEBUG: Received audio chunk ({len(message['bytes'])} bytes)")
                audio_bytes.extend(message["bytes"])
            elif "text" in message:
                print(f"[WS] Received text command: {message['text']}", flush=True)
                data = json.loads(message["text"])
                if data.get("type") == "end":
                    # The moment the user stops speaking, we instantly transcribe the accumulated stream!
                    await websocket.send_text(json.dumps({"status": "Processing", "message": "Transcribing audio..."}))
                    
                    stt_result = await transcribe_audio(bytes(audio_bytes))
                    recognized_text = stt_result.get("text")
                    user_lang = stt_result.get("language")
                    
                    if not recognized_text:
                        print(f"[WS] STT Failed - No text recognized", flush=True)
                        await websocket.send_text(json.dumps({"status": "Error", "message": "Could not recognize speech."}))
                        break
                        
                    await websocket.send_text(json.dumps({"transcript": recognized_text, "status": "Processing", "message": "Generating AI response live..."}))
                    
                    # Run the newly optimized 1-shot AI pipeline with Session ID
                    ai_result = await run_ai_pipeline(recognized_text, game_mode=gameMode, session_id=sessionId)
                    final_text = ai_result.get("final_response")
                    
                    await websocket.send_text(json.dumps({"aiResponse": final_text}))
                    
                    # Generate TTS
                    output_audio_bytes = await synthesize_speech(final_text, language_code=user_lang)
                    
                    # Feed binary audio bytes cleanly right back down the websocket!
                    await websocket.send_bytes(output_audio_bytes)
                    
                    # Reset audio buffer after processing one turn
                    audio_bytes.clear()
                    # We don't break here so the user can continue typing or speaking in the same session
                    
                elif data.get("type") == "text_query":
                    query_text = data.get("text")
                    print(f"[WS] Querying AI: {query_text}", flush=True)
                    await websocket.send_text(json.dumps({"status": "Processing", "message": "Thinking..."}))
                    
                    # Use the same AI pipeline
                    ai_result = await run_ai_pipeline(query_text, game_mode=gameMode, session_id=sessionId)
                    final_text = ai_result.get("final_response")
                    
                    await websocket.send_text(json.dumps({"aiResponse": final_text}))
                    
                    # Generate TTS for text queries
                    detected_lang = "en" # Fallback for text
                    output_audio_bytes = await synthesize_speech(final_text, language_code=detected_lang)
                    await websocket.send_bytes(output_audio_bytes)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            await websocket.send_text(json.dumps({"status": "Error", "message": str(e)}))
        except:
            pass

@router.post("/process-audio")
async def process_voice_audio(
    audio_file: UploadFile = File(...),
    game_mode: str | None = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Main pipeline entry for the Multilingual AI Voice Agent:
    1. STT (Google)
    2. Lang detection & translation to EN (OpenAI)
    3. Generate response with Knowledge Base (OpenAI)
    4. Translate EN -> User Lang (OpenAI)
    5. TTS (Google)
    6. Log data & Return Audio (GCS + FastAPI StreamingResponse)
    """
    try:
        # Step 1: Read audio bytes from user
        audio_bytes = await audio_file.read()
        session_id = str(uuid.uuid4())
        
        # Log to Storage
        await upload_to_gcs(f"inputs/{session_id}.wav", audio_bytes)
        
        # Step 2: Speech Recognition
        stt_result = await transcribe_audio(audio_bytes)
        recognized_text = stt_result.get("text")
        user_lang = stt_result.get("language")
        
        if not recognized_text:
            raise HTTPException(status_code=400, detail="Could not recognize speech.")
            
        # Steps 3, 4, 5: AI Processing Pipeline
        ai_result = await run_ai_pipeline(recognized_text, game_mode=game_mode)
        final_text = ai_result.get("final_response")
        
        # Step 6: Text-To-Speech Synthesis (OpenAI TTS)
        output_audio_bytes = await synthesize_speech(final_text, language_code=user_lang)
        
        # Step 8 & 9: Data Logging and monitoring
        await log_interaction(
            session_id=session_id,
            user_id=current_user.get("uid"),
            query=recognized_text,
            response=final_text,
            user_language=user_lang
        )
        
        import urllib.parse
        # Step 7: Stream audio back to Flutter mobile app
        return StreamingResponse(
            io.BytesIO(output_audio_bytes), 
            media_type="audio/wav", 
            headers={
                "X-Detected-Language": urllib.parse.quote(str(user_lang)),
                "X-Transcript": urllib.parse.quote(str(recognized_text)),
                "X-Response-Text": urllib.parse.quote(str(final_text))
            }
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
