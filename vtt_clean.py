#!/usr/bin/env python3
"""
vtt_clean.py — VTT Lecture Transcript Preprocessor
Strips UUID cue IDs, merges consecutive cues into ~60-second blocks,
and outputs clean text ready to paste into an LLM.

Usage:
    python3 vtt_clean.py "path/to/lecture.vtt"
    python3 vtt_clean.py "path/to/lecture.vtt" --block-seconds 90
    python3 vtt_clean.py "path/to/lecture.vtt" --output custom_output.txt
"""

import re
import sys
import argparse
from pathlib import Path


UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(-\d+)?$',
    re.IGNORECASE
)
TIMESTAMP_RE = re.compile(
    r'^(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*'
    r'(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})'
)
# Match lines that are pure noise: NOTE, WEBVTT header, positional tags, etc.
NOISE_RE = re.compile(r'^(WEBVTT|NOTE\b|STYLE\b|REGION\b)')
POSITION_TAG_RE = re.compile(r'<[^>]+>')      # <00:05:11.560>, <c>, </c>, etc.
FILLER_RE = re.compile(                        # repeated filler phrases
    r'\b(é+\s*,?\s*){2,}|\b(ã+\s*,?\s*){2,}',
    re.IGNORECASE
)


def timestamp_to_seconds(h, m, s, ms='0'):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_hms(total_seconds):
    total_seconds = int(total_seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def clean_text(text: str) -> str:
    text = POSITION_TAG_RE.sub('', text)   # strip inline timing tags
    text = text.strip()
    return text


def parse_vtt(path: Path):
    """
    Yields (start_seconds, text) tuples for every non-empty cue.
    Skips UUID cue IDs, WEBVTT/NOTE headers, and blank lines.
    """
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Skip header, NOTE blocks, STYLE blocks, blank lines, UUID lines
        if not line.strip():
            i += 1
            continue
        if NOISE_RE.match(line):
            # Skip until blank line (end of block)
            while i < len(lines) and lines[i].strip():
                i += 1
            continue
        if UUID_RE.match(line.strip()):
            i += 1
            continue

        # Try to parse as a timestamp line
        m = TIMESTAMP_RE.match(line.strip())
        if m:
            start_sec = timestamp_to_seconds(m.group(1), m.group(2), m.group(3))
            # Collect text lines that follow
            i += 1
            cue_lines = []
            while i < len(lines) and lines[i].strip():
                cue_lines.append(clean_text(lines[i].rstrip('\n')))
                i += 1
            text = ' '.join(t for t in cue_lines if t)
            if text:
                yield start_sec, text
            continue

        i += 1


def merge_into_blocks(cues, block_seconds=60):
    """
    Groups cues into blocks of ~block_seconds seconds.
    Each block starts a new paragraph with a [HH:MM:SS] header.
    """
    if not cues:
        return []

    blocks = []
    current_start = cues[0][0]
    current_texts = []
    block_boundary = cues[0][0] + block_seconds

    for start_sec, text in cues:
        if start_sec >= block_boundary and current_texts:
            blocks.append((current_start, ' '.join(current_texts)))
            current_start = start_sec
            current_texts = [text]
            block_boundary = start_sec + block_seconds
        else:
            current_texts.append(text)

    if current_texts:
        blocks.append((current_start, ' '.join(current_texts)))

    return blocks


def dedupe_consecutive(text: str) -> str:
    """Remove immediately repeated phrases (common in auto-captions)."""
    # Split on sentence boundaries and remove consecutive duplicates
    parts = re.split(r'(?<=[.!?])\s+', text)
    seen = []
    for part in parts:
        if not seen or part.strip().lower() != seen[-1].strip().lower():
            seen.append(part)
    return ' '.join(seen)


def format_blocks(blocks) -> str:
    lines = []
    for start_sec, text in blocks:
        ts = seconds_to_hms(start_sec)
        text = dedupe_consecutive(text)
        lines.append(f"[{ts}] {text}")
        lines.append("")   # blank line between blocks
    return '\n'.join(lines).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(
        description='Clean a VTT lecture transcript for LLM input.'
    )
    parser.add_argument('vtt_file', help='Path to the .vtt file')
    parser.add_argument(
        '--block-seconds', type=int, default=60, metavar='N',
        help='Seconds per paragraph block (default: 60)'
    )
    parser.add_argument(
        '--output', '-o', metavar='FILE',
        help='Output file path (default: <input>_clean.txt)'
    )
    parser.add_argument(
        '--stdout', action='store_true',
        help='Print to stdout instead of writing a file'
    )
    args = parser.parse_args()

    vtt_path = Path(args.vtt_file)
    if not vtt_path.exists():
        print(f"Error: file not found: {vtt_path}", file=sys.stderr)
        sys.exit(1)
    if vtt_path.suffix.lower() != '.vtt':
        print(f"Warning: file does not have .vtt extension: {vtt_path}", file=sys.stderr)

    print(f"Parsing: {vtt_path.name}", file=sys.stderr)
    cues = list(parse_vtt(vtt_path))
    print(f"  Cues found: {len(cues)}", file=sys.stderr)

    blocks = merge_into_blocks(cues, block_seconds=args.block_seconds)
    print(f"  Blocks ({args.block_seconds}s each): {len(blocks)}", file=sys.stderr)

    output = format_blocks(blocks)

    # Rough token estimate (Portuguese averages ~4 chars/token)
    token_estimate = len(output) // 4
    print(f"  Output size: {len(output):,} chars (~{token_estimate:,} tokens)", file=sys.stderr)

    if args.stdout:
        print(output)
    else:
        out_path = Path(args.output) if args.output else vtt_path.with_name(
            vtt_path.stem + '_clean.txt'
        )
        out_path.write_text(output, encoding='utf-8')
        print(f"  Saved to: {out_path}", file=sys.stderr)
        print(f"\nDone. Paste {out_path.name} into Claude.ai with the prompt from prompts/study-notes.md", file=sys.stderr)


if __name__ == '__main__':
    main()
