#!/usr/bin/env python3
"""
srt_to_vtt.py — Convert SRT subtitle file to WebVTT format
Converts the .srt output from LocalVocal (OBS plugin) to .vtt
so it can be processed by vtt_clean.py.

Usage:
    python3 scripts/srt_to_vtt.py aula.srt
    python3 scripts/srt_to_vtt.py aula.srt --output aula.vtt
"""

import re
import sys
import argparse
import unicodedata
from pathlib import Path

def slugify(name: str) -> str:
    """Convert a messy filename stem into a clean lowercase-hyphenated slug."""
    # Decompose unicode accents, keep ASCII equivalents
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ascii', errors='ignore').decode('ascii')
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name


TIMESTAMP_RE = re.compile(
    r'(\d{2}:\d{2}:\d{2}),(\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}),(\d{3})'
)


def srt_to_vtt(srt_path: Path) -> str:
    content = srt_path.read_text(encoding='utf-8', errors='replace')

    # Replace SRT timestamps (comma ms separator) with VTT (dot ms separator)
    vtt_body = TIMESTAMP_RE.sub(r'\1.\2 --> \3.\4', content)

    # Remove numeric cue IDs (lines that are just a number before a timestamp)
    lines = vtt_body.splitlines()
    cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip pure-numeric lines that appear right before a timestamp line
        if (line.strip().isdigit()
                and i + 1 < len(lines)
                and '-->' in lines[i + 1]):
            i += 1
            continue
        cleaned.append(line)
        i += 1

    return 'WEBVTT\n\n' + '\n'.join(cleaned).lstrip('\n')


def main():
    parser = argparse.ArgumentParser(
        description='Convert SRT (from LocalVocal/OBS) to WebVTT format.'
    )
    parser.add_argument('srt_file', help='Path to the .srt file')
    parser.add_argument(
        '--output', '-o', metavar='FILE',
        help='Output .vtt path (default: same name with .vtt extension)'
    )
    args = parser.parse_args()

    srt_path = Path(args.srt_file)
    if not srt_path.exists():
        print(f"Error: file not found: {srt_path}", file=sys.stderr)
        sys.exit(1)

    vtt_content = srt_to_vtt(srt_path)

    out_path = Path(args.output) if args.output else Path(slugify(srt_path.stem) + '.vtt')
    out_path.write_text(vtt_content, encoding='utf-8')

    print(f"Converted: {srt_path.name} → {out_path.name}", file=sys.stderr)
    print(f"Next: python3 scripts/vtt_clean.py \"{out_path}\"", file=sys.stderr)


if __name__ == '__main__':
    main()
