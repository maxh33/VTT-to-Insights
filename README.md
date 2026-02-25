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

After VTT-to-Insights: **~32k tokens**, clean paragraphs with timestamps.

---

## Features

- **Noise Reduction** — Removes UUIDs, WEBVTT headers, inline timing tags, blank lines
- **Token Optimization** — Shrinks file size 60–70% to fit within AI context windows
- **Smart Merging** — Converts fragmented cues into readable ~60-second paragraph blocks
- **Timestamp Preservation** — Every block keeps its `[HH:MM:SS]` marker for video navigation
- **Bilingual Prompt Library** — Ready-made prompts in English and Portuguese
- **Zero Dependencies** — Pure Python 3 standard library, no `pip install` needed
- **Cross-Platform** — Works on Windows, Mac, and Linux
- **Batch Ready** — Process an entire semester's worth of VTTs with a single command

---

## Installation

### Step 1 — Install Python

> **Already have Python?** Open a terminal and run `python3 --version` (Mac/Linux) or `python --version` (Windows). If you see `Python 3.x.x`, skip to Step 2.

**Windows**

1. Go to **[python.org/downloads](https://www.python.org/downloads/)** and click "Download Python 3.x.x"
2. Run the installer
3. **Critical:** At the bottom of the installer, check **"Add python.exe to PATH"** before clicking Install
4. Open **Command Prompt**: press `Win+R`, type `cmd`, press Enter
5. Verify it worked: `python --version` → should print `Python 3.x.x`

> On Windows, use `python` instead of `python3` in all commands below.

**Mac**

1. Open **Terminal**: press `Cmd+Space`, type `Terminal`, press Enter
2. Install via Homebrew (recommended):
   ```bash
   # Install Homebrew first (if you don't have it)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   # Then install Python
   brew install python3
   ```
   Or download the installer directly from [python.org/downloads](https://www.python.org/downloads/)
3. Verify: `python3 --version`

**Linux** (Ubuntu / Debian / Pop!\_OS)

```bash
sudo apt update && sudo apt install python3
```

For Fedora / RHEL:
```bash
sudo dnf install python3
```

Verify: `python3 --version`

---

### Step 2 — Download VTT-to-Insights

**Option A — Using Git** (recommended)

```bash
git clone https://github.com/maxh33/VTT-to-Insights.git
cd VTT-to-Insights
```

**Option B — Download ZIP**

Click the green **Code** button on [github.com/maxh33/VTT-to-Insights](https://github.com/maxh33/VTT-to-Insights) → **Download ZIP** → extract the folder.

No `pip install` required — the script uses only Python's built-in libraries.

---

## Quick Start

### Run the script

**Linux / Mac**
```bash
python3 vtt_clean.py "My Lecture 2024-02-04.vtt"
```

**Windows (Command Prompt)**
```cmd
python vtt_clean.py "My Lecture 2024-02-04.vtt"
```

**Windows (PowerShell)**
```powershell
python vtt_clean.py "My Lecture 2024-02-04.vtt"
```

> **Tip:** Drag and drop the `.vtt` file onto your terminal window to auto-paste its full path.

> **Windows tip:** If `python` isn't recognized, try `py vtt_clean.py "..."` instead.

**What you'll see in the terminal:**

```
──────────────────────────────────────────────────────
  VTT-to-Insights  ·  My Lecture 2024-02-04.vtt
──────────────────────────────────────────────────────
                            BEFORE        AFTER    SAVED
  Lines / blocks            11,247       166 blk
  Tokens (est.)            ~98,000      ~32,428      67%
  File size (KB)            381.3       126.7      67%
──────────────────────────────────────────────────────
  Saved : My Lecture 2024-02-04_clean.txt
  Folder: /path/to/your/lectures
  Next  : open a prompt from prompts/en/ or prompts/pt-BR/
          paste My Lecture 2024-02-04_clean.txt into Claude / Gemini / ChatGPT
──────────────────────────────────────────────────────
```

A 3-hour lecture goes from ~98,000 noisy tokens down to ~32,000 clean ones — a **67% reduction** that fits comfortably in any AI context window.

---

### VTT file in a different folder

You don't need to move your `.vtt` file into the project folder. Pass the full path to the file directly — the script works from anywhere.

> **Tip:** Drag and drop the `.vtt` file onto your terminal window to paste its full path automatically.
> **Tip:** Press `Tab` to autocomplete folder and file names while typing.

**Linux**
```bash
# File in ~/Documents
python3 ~/VTT-to-Insights/vtt_clean.py ~/Documents/lecture.vtt

# File on a mounted drive or university cloud folder
python3 ~/VTT-to-Insights/vtt_clean.py "/mnt/storage/University/Semester 1/lecture.vtt"
```

**Mac**
```bash
# File in Downloads
python3 ~/VTT-to-Insights/vtt_clean.py ~/Downloads/lecture.vtt

# File in a course folder inside Documents
python3 ~/VTT-to-Insights/vtt_clean.py "/Users/yourname/Documents/University/Semester 1/lecture.vtt"

# File in iCloud Drive
python3 ~/VTT-to-Insights/vtt_clean.py ~/Library/Mobile\ Documents/com~apple~CloudDocs/lecture.vtt
```

**Windows (Command Prompt)**
```cmd
python C:\Users\YourName\VTT-to-Insights\vtt_clean.py "C:\Users\YourName\Downloads\lecture.vtt"
python C:\Users\YourName\VTT-to-Insights\vtt_clean.py "C:\Users\YourName\Documents\University\Semester 1\lecture.vtt"
```

**Windows (PowerShell)**
```powershell
python C:\Users\YourName\VTT-to-Insights\vtt_clean.py "C:\Users\YourName\Downloads\lecture.vtt"
python C:\Users\YourName\VTT-to-Insights\vtt_clean.py "C:\Users\YourName\Documents\University\Semester 1\lecture.vtt"
```

> **Always keep the command on a single line.** Splitting with `\` + Enter causes a "file not found" error because the shell adds a leading space to the path.

> **Output location:** The `_clean.txt` file is saved next to your `.vtt` file — not in the project folder.

---

## Using the Prompts

After the script creates your `_clean.txt` file:

1. **Open** `_clean.txt` in any text editor (Notepad, TextEdit, VS Code) → **Select All** (`Ctrl+A` / `Cmd+A`) → **Copy** (`Ctrl+C` / `Cmd+C`)
2. **Open** one of the prompt files from the `prompts/en/` folder (e.g., `prompts/en/study-notes.md`)
3. **Copy** the text inside the ` ``` ` code block (that's your prompt)
4. Go to **[claude.ai](https://claude.ai)** (or chatgpt.com / gemini.google.com) → start a **New chat**
5. **Paste** the prompt into the chat message box
6. Scroll to the bottom of the prompt, **replace** `[PASTE THE CONTENT OF _clean.txt HERE]` with the transcript you copied in step 1
7. **Send** — wait ~30 seconds — your structured study notes appear

---

## Prompt Library

| Prompt | Language | Use Case | Output Length |
|--------|----------|----------|--------------|
| [`prompts/en/study-notes.md`](prompts/en/study-notes.md) | 🇬🇧 English | Full 5-section academic analysis | ~5 min read |
| [`prompts/en/quick-summary.md`](prompts/en/quick-summary.md) | 🇬🇧 English | 5-bullet overview | ~1 min read |
| [`prompts/en/concepts-only.md`](prompts/en/concepts-only.md) | 🇬🇧 English | Concept glossary / terminology | ~3 min read |
| [`prompts/pt-BR/study-notes.md`](prompts/pt-BR/study-notes.md) | 🇧🇷 Português | Análise acadêmica completa | ~5 min |
| [`prompts/pt-BR/quick-summary.md`](prompts/pt-BR/quick-summary.md) | 🇧🇷 Português | Resumo rápido em 5 pontos | ~1 min |
| [`prompts/pt-BR/concepts-only.md`](prompts/pt-BR/concepts-only.md) | 🇧🇷 Português | Glossário de conceitos | ~3 min |

See [`examples/sample_output.md`](examples/sample_output.md) for a real example of what the AI produces.

---

## Output Format

The cleaned file has one paragraph block per ~60 seconds, each with a timestamp:

```
[00:03:10] A partir de hoje a gente vai começar um pouco teórico,
como construir ali um conhecimento para depois desse conhecimento,
tendo aquela base estruturada, a gente consiga fazer colocar em
prática ali. A gente vai mexer com Figma...

[00:05:11] O fundamento de IHC é a organização e arquitetura
aplicada ao computador humano. Interação humano computador...
```

---

## All Options

```
python3 vtt_clean.py [OPTIONS] vtt_file

positional arguments:
  vtt_file              Path to the .vtt file

options:
  --block-seconds N     Seconds per paragraph block (default: 60)
  --output FILE, -o     Custom output file path
  --stdout              Print to stdout instead of writing a file
  -h, --help            Show this help message
```

**More examples:**

```bash
# Larger blocks — less fragmented, better for long monologues
python3 vtt_clean.py lecture.vtt --block-seconds 90

# Save to a specific location (Linux/Mac)
python3 vtt_clean.py lecture.vtt --output ~/Desktop/clean.txt

# Save to a specific location (Windows)
python vtt_clean.py lecture.vtt --output "C:\Users\You\Desktop\clean.txt"

# Copy output directly to clipboard (Mac)
python3 vtt_clean.py lecture.vtt --stdout | pbcopy

# Copy output directly to clipboard (Linux)
python3 vtt_clean.py lecture.vtt --stdout | xclip -selection clipboard

# Batch process all VTTs in a folder (Linux/Mac)
for f in lectures/*.vtt; do python3 vtt_clean.py "$f"; done

# Batch process all VTTs in a folder (Windows PowerShell)
Get-ChildItem -Filter *.vtt | ForEach-Object { python vtt_clean.py $_.FullName }
```

---

## Platform Notes

| Platform | Python command | Terminal to open |
|----------|---------------|-----------------|
| Windows | `python` or `py` | Command Prompt (`cmd`) or PowerShell |
| Mac | `python3` | Terminal (Cmd+Space → "Terminal") |
| Linux | `python3` | Your distro's terminal emulator |

> **Windows path tip:** Use quotes around paths with spaces: `python vtt_clean.py "C:\My Lectures\week1.vtt"`

---

## VTT Source Compatibility

Tested with VTT files exported from:
- **Microsoft Teams** (university portals, recorded meetings)
- **Zoom** (auto-generated captions)
- **Google Meet** (with caption recording enabled)
- **YouTube** (auto-generated — download with `yt-dlp --write-auto-sub --sub-lang en URL`)

---

## Project Structure

```
VTT-to-Insights/
├── vtt_clean.py               ← Main script (no dependencies)
├── prompts/
│   ├── en/                    ← English prompts
│   │   ├── study-notes.md
│   │   ├── quick-summary.md
│   │   └── concepts-only.md
│   └── pt-BR/                 ← Portuguese prompts
│       ├── study-notes.md
│       ├── quick-summary.md
│       └── concepts-only.md
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
- Translations to other languages

Open an issue or submit a PR at [github.com/maxh33/VTT-to-Insights](https://github.com/maxh33/VTT-to-Insights).

---

## License

MIT — see [LICENSE](LICENSE)

---

*This project was born in a Computer Science classroom in Brazil 🇧🇷 to help students worldwide manage long lecture transcripts. Contributions are welcome!*

<!-- GitHub Topics: vtt-converter transcription ai-summarization study-tools productivity python gpt-prompting lecture-notes -->
