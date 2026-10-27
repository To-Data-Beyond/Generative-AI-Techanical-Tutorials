import argparse
from pathlib import Path
from gtts import gTTS, gTTSError

def text_to_audio(text_file_path, output_audio_path):
    text = Path(text_file_path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Input text is empty")
    gTTS(text=text, lang="en", timeout=(10, 30)).save(str(output_audio_path))
    return Path(output_audio_path)

def main():
    parser = argparse.ArgumentParser(description="Convert owned English text to MP3 using Google Translate TTS.")
    parser.add_argument("text_file", type=Path)
    parser.add_argument("output_audio", type=Path)
    args = parser.parse_args()
    try:
        output = text_to_audio(args.text_file, args.output_audio)
        print(f"Created {output.name}: {output.stat().st_size} bytes")
    except (OSError, ValueError, gTTSError) as exc:
        parser.exit(1, f"Text-to-speech failed: {exc}\n")

if __name__ == "__main__":
    main()
