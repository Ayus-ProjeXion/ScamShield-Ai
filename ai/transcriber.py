"""
ScamShield AI — Audio Call Voice Transcriber (Whisper STT with SpeechRecognition Fallback)
Converts voice recordings, phone call audio, and voice notes into text for threat detection.
"""

import os
import sys
from typing import Dict, Any, Optional

def transcribe_audio(audio_path: str, model_size: str = "tiny") -> Dict[str, Any]:
    """
    Transcribes an audio file into text using OpenAI Whisper or SpeechRecognition fallback.
    
    Args:
        audio_path: Path to the .wav, .mp3, or .m4a audio file.
        model_size: Whisper model size ('tiny', 'base', 'small').
        
    Returns:
        dict containing:
            - 'text': Transcribed text string
            - 'engine': 'whisper' or 'speech_recognition'
            - 'language': Detected language (e.g. 'en')
            - 'success': Boolean status
    """
    if not os.path.exists(audio_path):
        return {
            "success": False,
            "text": "",
            "engine": "none",
            "error": f"Audio file not found: {audio_path}"
        }

    # 1. Attempt OpenAI Whisper
    try:
        import whisper
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path)
        return {
            "success": True,
            "text": result.get("text", "").strip(),
            "engine": f"whisper-{model_size}",
            "language": result.get("language", "en"),
            "segments": len(result.get("segments", [])),
        }
    except ImportError:
        pass
    except Exception as e:
        sys.stderr.write(f"Whisper inference notice: {e}. Falling back to SpeechRecognition.\n")

    # 2. Fallback to SpeechRecognition (Local / Google Speech)
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return {
                "success": True,
                "text": text.strip(),
                "engine": "speech_recognition_google",
                "language": "en",
            }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "engine": "speech_recognition_fallback",
            "error": f"Audio transcription failed: {str(e)}"
        }

if __name__ == "__main__":
    print("ScamShield Audio Transcriber initialized.")
    print("Supports: Whisper (tiny/base) with automated SpeechRecognition fallback.")
