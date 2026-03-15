# Prompt: Full Lecture Analysis (Academic Study Notes)

> **How to use:**
> 1. Run `python3 scripts/vtt_clean.py "your_lecture.vtt"` to generate the `_clean.txt` file
> 2. Open the `_clean.txt` file → select all → copy
> 3. Go to [claude.ai](https://claude.ai) (or ChatGPT / Gemini) → start a new chat
> 4. (Optional) Paste the **System Prompt** below into the chat's system settings
> 5. Paste the **User Prompt**, replace `[COURSE NAME]` with your subject name
> 6. Paste the content of `_clean.txt` at the bottom where indicated
> 7. Send — wait ~30 seconds — read your structured study notes

---

## System Prompt

```
You are an academic study assistant specialized in analyzing university lecture
transcripts. Your goal is to extract maximum study value from each lecture.
```

---

## User Prompt

```
Analyze the transcript below from a ~3-hour university lecture
(course: [COURSE NAME]).

Produce a structured analysis with the following sections:

## 📋 Topic Index
List each main topic with the timestamp where it begins.
Format: `[HH:MM:SS]` — Topic name

## 🔑 Key Concepts
List all definitions, concepts, frameworks, and technical terms introduced.
For each one, include:
- The concept name in bold
- A clear, objective definition
- The timestamp of the explanation

## ⭐ Essential Moments (Top 8–12)
Identify the highest study-value timestamps — where the instructor explains
something critical, gives a practical example, or demonstrates a technique.
For each moment:
- Timestamp
- One sentence explaining why this moment is important

## 📝 Activities and Exercises
List any task, practical activity, or exercise mentioned,
with the timestamp and enough context to understand what needs to be done.

## 📖 Lecture Summary
A concise 250–350 word summary covering:
- Central theme of the lecture
- Main concepts presented
- Connections between topics
- What was practical vs. theoretical

---
TRANSCRIPT:
[PASTE THE CONTENT OF _clean.txt HERE]
```
