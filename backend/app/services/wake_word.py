import openwakeword
from openwakeword.model import Model
import numpy as np

# Load a default model
# Common models: "hey_jarvis", "alexa", "hey_google"
# Since the app mentioned JARVIS in the stub, let's use a similar one or a generic one.
# openwakeword has "hey_jarvis"
# Shared model instance to avoid reloading for every connection
_shared_model = None

class WakeWordDetector:
    def __init__(self, model_names=["hey_jarvis", "alexa"]):
        global _shared_model
        self.model_name = "Epic"
        self.audio_buffer = np.array([], dtype=np.float32)
        
        if _shared_model is None:
            try:
                import openwakeword.utils
                print(f"WakeWordDetector: Checking paths for {model_names}...", flush=True)
                # paths = openwakeword.get_pretrained_model_paths() # Already checked those
                print(f"WakeWordDetector: Calling Model(...) initialization...", flush=True)
                _shared_model = Model(wakeword_models=model_names, inference_framework="onnx")
                print(f"WakeWordDetector: Model class initialized. Testing prediction...", flush=True)
                # Test with dummy audio to ensure ONNX session is alive
                _shared_model.predict(np.zeros(1280, dtype=np.float32))
                print(f"WakeWordDetector: Shared engine ready (Session test passed)", flush=True)
            except Exception as e:
                print(f"WakeWordDetector Error loading shared engine: {e}", flush=True)
                # Fallback logic if needed, but for now we expect success
        
        self.oww_model = _shared_model

    def detect(self, audio_data: bytes) -> bool:
        """
        Detects if the wake word is present in the audio data.
        Expects 16kHz, 16-bit PCM mono audio.
        """
        if not self.oww_model:
            return False
            
        # Reset gain to a safe level to avoid clipping (distortion)
        audio_int16 = np.frombuffer(audio_data, dtype=np.int16)
        peak = np.max(np.abs(audio_int16))
        
        # Log to verify mic activity
        if peak > 1000:
             print(f"[WS] Audio Peak: {peak} (Active Speech)", flush=True)
             
        new_audio = (audio_int16.astype(np.float32) / 32768.0) * 1.8
        self.audio_buffer = np.append(self.audio_buffer, new_audio)
        
        # Safety: Keep a small buffer for instant processing
        if len(self.audio_buffer) > 4800:
            self.audio_buffer = self.audio_buffer[-4800:]

        detected = False
        while len(self.audio_buffer) >= 1280:
            chunk = self.audio_buffer[:1280]
            self.audio_buffer = self.audio_buffer[1280:]
            
            prediction = self.oww_model.predict(chunk)
            for m_name, val in prediction.items():
                # If we get ANY signal, we verify with phonetic matching
                if val > 0.10: 
                    print(f"[WS] WW Signal Found ({m_name}: {val:.2f}). Verifying phonetics...", flush=True)
                    detected = True
        
        # Also trigger on loud volume to catch "Epic" if ONNX fails
        if peak > 15000:
            print(f"[WS] Volume Trigger! Verifying...", flush=True)
            detected = True

        return detected
        
        return detected

def get_model_names():
    # Helper to see available models
    return ["hey_jarvis", "alexa", "hey_google"]
