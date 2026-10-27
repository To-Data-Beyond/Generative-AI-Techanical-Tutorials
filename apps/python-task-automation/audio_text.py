import argparse
import os
from pathlib import Path
import certifi
import speech_recognition as sr

def transcribe_audio(audio_file_path):
    # Use a trusted CA bundle, never disable certificate verification.
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    recognizer = sr.Recognizer()
    recognizer.operation_timeout = 30
    with sr.AudioFile(str(audio_file_path)) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(
        audio, endpoint="https://www.google.com/speech-api/v2/recognize")

def main():
    parser = argparse.ArgumentParser(description="Transcribe an owned WAV/AIFF/FLAC audio file using Google speech recognition.")
    parser.add_argument("audio_file", type=Path)
    args = parser.parse_args()
    try:
        print(transcribe_audio(args.audio_file))
    except (OSError, ValueError, sr.UnknownValueError, sr.RequestError) as exc:
        parser.exit(1, f"Transcription failed: {exc}\n")

if __name__ == "__main__":
    main()
