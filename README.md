# VTT-to-Insights

**Turn 3-hour lecture transcripts into concise, AI-ready study notes in seconds.**

Stop reading through thousands of lines of `ums`, `ahs`, and UUID noise. VTT-to-Insights cleanses raw `.vtt` caption files — removing cue IDs, merging fragmented cues, and collapsing repetition — so you can feed clean, token-efficient context into your favourite LLM (Claude, ChatGPT, Gemini) for high-quality study summaries.

> Born in a Computer Science classroom in Brazil 🇧🇷 · [Leia em Português](README.pt-BR.md)

---

## The Problem

University portals export lecture recordings as `.vtt` files. A 3-hour lecture generates ~11,000 lines:

```
bde3c4a1-7f2e-4b1a-9c3d-000000000042-0     ← UUID noise (pure junk)
00:05:11.560 --> 00:05:16.738
O fundamento de IHC é a organização

bde3c4a1-7f2e-4b1a-9c3d-000000000043-0
00:05:16.738 --> 00:05:19.200
e arquitetura aplicada ao computador
```

Raw token cost: **~85k–100k tokens**. Too noisy for useful LLM output.

After VTT-to-Insights: **~55k–65k tokens**, clean paragraphs with timestamps.

---

## Features

- **Noise Reduction** — Removes UUIDs, WEBVTT headers, inline timing tags, blank lines
- **Token Optimization** — Shrinks file size 30–40% to fit within AI context windows
- **Smart Merging** — Converts fragmented cues into readable ~60-second paragraph blocks
- **Timestamp Preservation** — Every block keeps its `[HH:MM:SS]` marker for video navigation
- **Prompt Library** — Ready-made prompts for study notes, summaries, and concept extraction
- **Zero Dependencies** — Pure Python 3 standard library, no pip install needed
- **Batch Ready** — Process an entire semester's worth of VTTs with a shell loop

---

## Quick Start

```bash
# Clone
git clone https://github.com/yourusername/VTT-to-Insights.git
cd VTT-to-Insights

# Run (no dependencies required)
python3 vtt_clean.py "My Lecture 2024-02-04.vtt"
# → My Lecture 2024-02-04_clean.txt

# Then paste _clean.txt into Claude / ChatGPT with a prompt from prompts/
```

---

## Output Format

```
[00:03:10] A partir de hoje a gente vai começar um pouco teórico,
como construir ali um conhecimento para depois desse conhecimento,
tendo aquela base estruturada, a gente consiga fazer colocar em
prática ali. A gente vai mexer com Figma...

[00:05:11] O fundamento de IHC é a organização e arquitetura
aplicada ao computador humano. Interação humano computador...
```

---

## Prompt Library

| Prompt | Use Case | Time to Read |
|--------|----------|-------------|
| [`study-notes.md`](prompts/study-notes.md) | Full academic analysis (5 sections) | ~5 min |
| [`quick-summary.md`](prompts/quick-summary.md) | 5-bullet overview | ~1 min |
| [`concepts-only.md`](prompts/concepts-only.md) | Glossary / terminology | ~3 min |

See [`examples/sample_output.md`](examples/sample_output.md) for a real output example.

---

## Workflow

```
1. Download .vtt from your university portal        (~30 sec)
2. python3 vtt_clean.py "lecture.vtt"              (~5 sec)
3. Open Claude.ai / ChatGPT → New chat             (~10 sec)
4. Paste prompt + contents of _clean.txt            (~1 min)
5. Read structured output, jump to key timestamps   (study time)
```

---

## Options

```
python3 vtt_clean.py --help

positional arguments:
  vtt_file              Path to the .vtt file

options:
  --block-seconds N     Seconds per paragraph block (default: 60)
  --output FILE, -o     Custom output file path
  --stdout              Print to stdout (pipe-friendly)
```

**Examples:**
```bash
# Larger blocks (less fragmented)
python3 vtt_clean.py lecture.vtt --block-seconds 90

# Pipe directly into clipboard (Linux)
python3 vtt_clean.py lecture.vtt --stdout | xclip -selection clipboard

# Batch process a whole folder
for f in lectures/*.vtt; do python3 vtt_clean.py "$f"; done
```

---

## Compatibility

Tested with VTT files exported from:
- **Microsoft Teams** (university portals)
- **Zoom** (auto-generated captions)
- **Google Meet** (with caption recording)
- **YouTube** (auto-generated, download via `yt-dlp --write-auto-sub`)

---

## Project Structure

```
VTT-to-Insights/
├── vtt_clean.py               ← Main script (no dependencies)
├── prompts/
│   ├── study-notes.md         ← Full academic analysis prompt (Portuguese)
│   ├── quick-summary.md       ← 5-bullet quick summary prompt
│   └── concepts-only.md       ← Glossary / concepts extraction prompt
├── examples/
│   └── sample_output.md       ← Anonymized example output
├── README.md                  ← This file (English)
├── README.pt-BR.md            ← Full Portuguese documentation
└── LICENSE                    ← MIT
```

---

## Contributing

Contributions welcome! Especially:
- Support for additional VTT dialects
- Speaker diarization (separate speakers)
- More prompt templates (exam prep, mind map generation)
- Language support beyond Portuguese/English

Open an issue or submit a PR.

---

## License

MIT — see [LICENSE](LICENSE)

---

*This project was born in a Computer Science classroom in Brazil 🇧🇷 to help students worldwide manage long lecture transcripts. Contributions are welcome!*

<!-- GitHub Topics: vtt-converter transcription ai-summarization study-tools productivity python gpt-prompting lecture-notes -->
