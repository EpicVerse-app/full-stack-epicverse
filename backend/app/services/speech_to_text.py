import openai
import io
import wave
from app.core.config import settings

_client = None

def get_openai_client() -> openai.AsyncOpenAI:
    global _client
    if _client is None:
        _client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

async def transcribe_audio(audio_content: bytes, project_id: str = settings.GCP_PROJECT_ID, location: str = "global") -> dict:
    """
    Transcribes audio using OpenAI Whisper.
    Converts raw PCM16 bits into an in-memory WAV file before sending to OpenAI.
    """
    client = get_openai_client()
    
    # 1. Convert raw Android PCM stream to a valid WAV file in RAM
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(1)       # Mono channel
        wav_file.setsampwidth(2)       # 2 bytes per sample (16-bit)
        wav_file.setframerate(16000)   # 16kHz
        wav_file.writeframes(audio_content)
    
    wav_io.seek(0)
    
    # 2. Whisper requires a file-like tuple
    file_tuple = ("audio.wav", wav_io.read(), "audio/wav")
    
    response = await client.audio.transcriptions.create(
        model="whisper-1",
        file=file_tuple,
        response_format="verbose_json"
    )
    
    # The 'verbose_json' format returns the text and the detected language code natively.
    return {
        "text": response.text,
        "language": response.language
    }
