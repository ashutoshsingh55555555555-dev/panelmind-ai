"""Optional voice-answer transcription for interview practice."""

import io


def transcribe_audio(audio_bytes):
    """Transcribe a recorded WAV answer using Google's speech endpoint."""
    try:
        import speech_recognition as sr
    except ImportError as exc:
        raise RuntimeError(
            "Voice mode needs the SpeechRecognition package. "
            "Install the project requirements and try again."
        ) from exc

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        raise RuntimeError(
            "I could not understand that recording. Please record it again "
            "or type your answer instead."
        ) from None
    except sr.RequestError:
        raise RuntimeError(
            "Voice transcription is temporarily unavailable. "
            "Please type your answer instead."
        ) from None
