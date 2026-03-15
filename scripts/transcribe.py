#!/usr/bin/env python3
"""
transcribe.py — Transcribe audio/video to WebVTT using faster-whisper
Uses CUDA (NVIDIA GPU) when available for real-time or faster-than-real-time transcription.

Requirements:
    pip install faster-whisper

Usage:
    python3 scripts/transcribe.py aula.mp4
    python3 scripts/transcribe.py aula.mp4 --language pt --model large-v3
    python3 scripts/transcribe.py aula.mp3 --output aula.vtt
"""

import sys
import argparse
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def transcribe_to_vtt(input_path: Path, model_name: str, language: str) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Error: faster-whisper not installed.", file=sys.stderr)
        print("Run: pip install faster-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"Loading model '{model_name}'...", file=sys.stderr)
    model = WhisperModel(model_name, device="auto", compute_type="auto")

    print(f"Transcribing '{input_path.name}' (language={language or 'auto'})...", file=sys.stderr)
    segments, info = model.transcribe(
        str(input_path),
        language=language or None,
        beam_size=5,
        vad_filter=True,
    )

    print(f"Detected language: {info.language} (prob={info.language_probability:.2f})", file=sys.stderr)

    lines = ['WEBVTT', '']
    for seg in segments:
        start = format_timestamp(seg.start)
        end = format_timestamp(seg.end)
        text = seg.text.strip()
        if text:
            lines.append(f"{start} --> {end}")
            lines.append(text)
            lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio/video to WebVTT using faster-whisper + CUDA.'
    )
    parser.add_argument('input_file', help='Audio or video file (.mp4, .mp3, .wav, etc.)')
    parser.add_argument(
        '--model', default='large-v3',
        help='Whisper model (default: large-v3). Options: tiny, base, small, medium, large-v2, large-v3'
    )
    parser.add_argument(
        '--language', '--lang', default='pt',
        help='Language code (default: pt). Use "auto" for auto-detection.'
    )
    parser.add_argument(
        '--output', '-o', metavar='FILE',
        help='Output .vtt path (default: same name with .vtt extension)'
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    language = None if args.language == 'auto' else args.language
    vtt_content = transcribe_to_vtt(input_path, args.model, language)

    out_path = Path(args.output) if args.output else input_path.with_suffix('.vtt')
    out_path.write_text(vtt_content, encoding='utf-8')

    print(f"Saved: {out_path}", file=sys.stderr)
    print(f"Next: python3 scripts/vtt_clean.py \"{out_path}\"", file=sys.stderr)


if __name__ == '__main__':
    main()
