#!/usr/bin/env python3
"""
vtt_clean.py — VTT Lecture Transcript Preprocessor
Strips UUID cue IDs, merges consecutive cues into ~60-second blocks,
and outputs clean text ready to paste into an LLM.

Usage:
    python3 scripts/vtt_clean.py "path/to/lecture.vtt"
    python3 scripts/vtt_clean.py "path/to/lecture.vtt" --block-seconds 90
    python3 scripts/vtt_clean.py "path/to/lecture.vtt" --output custom_output.txt
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
FILLER_RE = re.compile(                        # repeated filler sounds
    r'\b(é+\s*,?\s*){2,}|\b(ã+\s*,?\s*){2,}',
    re.IGNORECASE
)
# Common Brazilian Portuguese spoken fillers (stripped when standalone or trailing)
VERBAL_FILLER_RE = re.compile(
    r'\bvamos dizer assim[,.]?\s*'
    r'|\bvamos dizer\b[,.]?\s*'
    r'|\btá[,?!]?\s*(?=\b|$)'
    r'|\bné[,?!]?\s*(?=\b|$)'
    r'|(?<! o )(?<!do )(?<!no )(?<!ao )\bpessoal[,?!]\s*'  # vocative (preserve 'o/do/no pessoal')
    r'|\btum\b[,.]?\s*'
    r'|(?<![aA] )(?<![Dd]a )\bgente[,?!]\s*'   # "gente" vocative (preserve "a gente")
    r'|\bó\b\s*'                                # standalone attention-getter
    r'|\bbom[?!]\s*'                             # "bom?" discourse marker
    r'|\b[Tt]udo bem[?!]\s*'                    # repeated "Tudo bem?"
    r'|\bok\?\s*'                              # "ok?" as filler
    r'|\bÉ[,\.]{1,3}\s+'                       # "É..." / "É, " hesitation
    r'|\bah\b[,.]?\s*'                          # "ah" interjection
    r'|\beh\b[,.]?\s*',                         # "eh" interjection
    re.IGNORECASE
)
# Cleanup leftover punctuation artifacts after filler removal
PUNCT_CLEANUP_RE = re.compile(r'\s*,\s*,|,\s*(?=[.!?])')
# Repeated consecutive words: "décadas, décadas, décadas" → "décadas"
REPEATED_WORD_RE = re.compile(
    r'\b(\w{3,})[,.]?\s+(?:\1[,.]?\s*){2,}',
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
    text = FILLER_RE.sub('', text)
    text = VERBAL_FILLER_RE.sub('', text)
    text = REPEATED_WORD_RE.sub(r'\1', text)
    text = PUNCT_CLEANUP_RE.sub(',', text)
    text = re.sub(r'\s{2,}', ' ', text)   # collapse extra spaces
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


def clean_block(text: str) -> tuple[str, list[str]]:
    """Post-merge cleaning: removes fillers and repeated words within a full block.
    Returns (cleaned_text, list_of_detected_repetitions)."""
    warnings = [m.group(0).strip() for m in REPEATED_WORD_RE.finditer(text)]
    text = VERBAL_FILLER_RE.sub('', text)
    text = REPEATED_WORD_RE.sub(r'\1', text)
    text = PUNCT_CLEANUP_RE.sub(',', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip(), warnings


def format_blocks(blocks) -> tuple[str, list[tuple]]:
    lines = []
    hallucinations = []   # [(timestamp_str, pattern), ...]
    for start_sec, text in blocks:
        ts = seconds_to_hms(start_sec)
        text = dedupe_consecutive(text)
        text, warnings = clean_block(text)
        for w in warnings:
            hallucinations.append((ts, w))
        lines.append(f"[{ts}] {text}")
        lines.append("")   # blank line between blocks
    return '\n'.join(lines).rstrip() + '\n', hallucinations


def print_summary(filename, raw_lines, raw_tokens, raw_chars,
                  n_blocks, block_seconds, out_tokens, out_chars,
                  hallucinations=None, out_path=None, to_stdout=False):
    token_saved_pct = round((1 - out_tokens / raw_tokens) * 100) if raw_tokens else 0
    size_saved_pct  = round((1 - out_chars  / raw_chars)  * 100) if raw_chars  else 0
    sep = "─" * 54

    def p(msg=""):
        print(msg, file=sys.stderr)

    p(sep)
    p(f"  VTT-to-Insights  ·  {filename}")
    p(sep)
    p(f"  {'':20}  {'BEFORE':>10}   {'AFTER':>10}   {'SAVED':>6}")
    raw_tok_str = f"~{raw_tokens:,}"
    out_tok_str = f"~{out_tokens:,}"
    p(f"  {'Lines / blocks':20}  {raw_lines:>10,}   {n_blocks:>7,} blk")
    p(f"  {'Tokens (est.)':20}  {raw_tok_str:>10}   {out_tok_str:>10}   {token_saved_pct:>5}%")
    p(f"  {'File size (KB)':20}  {raw_chars/1024:>9.1f}   {out_chars/1024:>9.1f}   {size_saved_pct:>5}%")
    p(sep)
    if hallucinations:
        p(f"  ⚠  {len(hallucinations)} repetição(ões) detectada(s) — possível alucinação do ASR:")
        for ts, pattern in hallucinations:
            preview = pattern[:50] + ('…' if len(pattern) > 50 else '')
            p(f"     [{ts}] \"{preview}\"")
        p(f"  Revise esses trechos no vídeo original.")
        p(sep)
    if not to_stdout and out_path:
        p(f"  Saved : {out_path.name}")
        p(f"  Folder: {out_path.parent}")
        p(f"  Next  : open a prompt from prompts/en/ or prompts/pt-BR/")
        p(f"          paste {out_path.name} into Claude / Gemini / ChatGPT")
        p(sep)


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

    # Capture raw stats for before/after comparison
    raw_content = vtt_path.read_text(encoding='utf-8', errors='replace')
    raw_lines = raw_content.count('\n') + 1
    raw_chars = len(raw_content)
    raw_tokens = raw_chars // 4

    cues = list(parse_vtt(vtt_path))
    blocks = merge_into_blocks(cues, block_seconds=args.block_seconds)
    output, hallucinations = format_blocks(blocks)

    # Rough token estimate (Portuguese averages ~4 chars/token)
    token_estimate = len(output) // 4

    if args.stdout:
        print(output)
        out_path = None
    else:
        out_path = Path(args.output) if args.output else vtt_path.with_name(
            vtt_path.stem + '_clean.txt'
        )
        out_path.write_text(output, encoding='utf-8')

    print_summary(
        filename=vtt_path.name,
        raw_lines=raw_lines, raw_tokens=raw_tokens, raw_chars=raw_chars,
        n_blocks=len(blocks), block_seconds=args.block_seconds,
        out_tokens=token_estimate, out_chars=len(output),
        hallucinations=hallucinations,
        out_path=out_path,
        to_stdout=args.stdout,
    )


if __name__ == '__main__':
    main()
