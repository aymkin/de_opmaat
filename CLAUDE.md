# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Purpose

This is a Dutch language learning materials directory for the "De Opmaat" course
(NT2 - Nederlands als Tweede Taal, targeting A2 level). It contains vocabulary
lists, tests, audio files, Anki flashcard materials, and supplementary
documents.

## Directory Structure

- `thema_1/` through `thema_7/` - Course materials organized by theme/chapter
- `daily/` - Daily practice sessions with dated subfolders (e.g.,
  `11_dec_2025/`)
- `stories/` - Narrative exercises with bolded verbs and grammar patterns
- `transcriptions/` - Audio transcripts
- `existin_not_sorted/` - Raw/unsorted learning materials and vocabulary exports
- `other/` - Administrative documents and learning methodology notes

## Commands

```bash
npm run format        # Format all markdown files with Prettier
npm run format:check  # Check formatting without changes
```

## File Naming Conventions

| Pattern                            | Example                                  | Purpose                   |
| ---------------------------------- | ---------------------------------------- | ------------------------- |
| `{N}_opdracht.md`                  | `6_opdracht.md`                          | Numbered exercises        |
| `woordenlijst_pagina_{N}_anki.txt` | `woordenlijst_pagina_16_anki.txt`        | Vocabulary by page        |
| `grammatica_{topic}.md`            | `grammatica_praten_over_het_verleden.md` | Grammar explanations      |
| `taalhulp_{topic}_anki.txt`        | `taalhulp_klok_anki.txt`                 | Topic-specific flashcards |
| `verhaal_{NN}_{title}.md`          | `verhaal_01_de_reis_naar_amsterdam.md`   | Story exercises           |

## Common File Types

- `.pdf` - Vocabulary lists (woordenlijst), tests (toetsen), answer keys
  (beoordeling)
- `.mp3` - Audio exercises and listening materials
- `.md` - Exercises, grammar notes, error tracking, stories
- `*_anki.txt` - Anki flashcard format files (see format below)

## Anki File Formats

Files ending in `_anki.txt` use tab-separated format. Two variants exist:

**Full format** (vocabulary with audio):

```
#separator:tab
#html:true
#tags column:5
```

Fields: Dutch term | Russian translation | Notes | Audio | Tags

**Sentence-only format** (example sentences):

```
#separator:tab
#html:false
```

Fields: Dutch sentence | Russian translation

### Audio References

Audio files reference external TTS services:

- ElevenLabs: `[sound:elevenlabs_filename.mp3]`
- Amazon Polly: `[sound:polly_filename.mp3]`

### Construction Cards (Multisensory Format)

For language constructions (ready-made phrases), use the multisensory format
that activates multiple memory systems:

**File naming:** `constructies_{topic}_anki.txt`

**Header:**

```
#separator:tab
#html:true
#tags column:6
```

**Fields:** Russian prompt | Dutch construction | Context sentences | Image cue
| Audio | Tags

**Card template (front):**

```
🇷🇺 {{Russian prompt}}

💭 Где ты это используешь? (think before flipping)
```

**Card template (back):**

```
🇳🇱 {{Dutch construction}}

🔊 {{Audio}}

📝 {{Context sentences}}

🖼️ {{Image cue}}
```

**Example entry:**

```
Я хотел бы...	Ik zou graag...	- Ik zou graag een tafel reserveren.<br>- Ik zou graag meer informatie willen.	представь себя в ресторане	[sound:ik_zou_graag.mp3]	constructies::vragen::A2
```

**Construction categories for tags:**

| Category   | Tag prefix                | Examples                           |
| ---------- | ------------------------- | ---------------------------------- |
| Opinions   | `constructies::mening`    | Ik vind dat..., Naar mijn mening.. |
| Requests   | `constructies::vragen`    | Zou ik... mogen?, Kunt u...        |
| Causes     | `constructies::oorzaak`   | Omdat..., Daarom...                |
| Time/Order | `constructies::tijd`      | Ten eerste..., Uiteindelijk...     |
| Comparison | `constructies::contrast`  | Aan de ene kant..., Terwijl...     |
| Daily      | `constructies::dagelijks` | Hoeveel kost...?, Waar is...?      |
| Fillers    | `constructies::fillers`   | Nou..., Eigenlijk...               |

**Level tags:** Add `::A1`, `::A2`, or `::B1` suffix based on complexity.

**Reference:** See
`other/language_learning_methods/integrated_method_daily_routine.md` for the
full construction library (65+ phrases) organized by communicative function.

## Content Conventions

### Vocabulary

- Dutch nouns must include articles: `het stokbrood`, `de stroopwafel`
- Provide Russian translations; English as supplementary
- Show sentences in context (positive, negative, interrogative forms)

### Exercise Markdown Format

Use visual indicators for corrections:

- ✅ for correct answers
- ❌ for incorrect
- ~~strikethrough~~ for wrong parts with correction following

### Error Tracking Notes

Structure error notes with:

- Date stamp
- Sections: Spelling errors, Grammar rules, Frequency words
- Markdown tables showing: Error | Correction | Rule/Tip

### Story Files

Include:

- Narrative text with **bolded verbs** for pattern recognition
- Grammar summary tables
- Vocabulary list (Dutch → Russian → English)

## Grammar Reference

When explaining Dutch grammar, use tables for word order patterns:

| Conjunction | Word Order         | Example                            |
| ----------- | ------------------ | ---------------------------------- |
| **want**    | normal (S + V)     | Ik blijf thuis, want ik ben ziek.  |
| **omdat**   | verb to end        | Ik blijf thuis, omdat ik ziek ben. |
| **als**     | verb to end        | Als het regent, blijf ik thuis.    |
| (inversie)  | V + S after adverb | Morgen ga ik naar Amsterdam.       |

### Common Spelling Corrections

| Wrong      | Correct     | Note           |
| ---------- | ----------- | -------------- |
| capot      | kapot       | Dutch uses 'k' |
| stroopdas  | stropdas    | Single 'o'     |
| de station | het station | het-woord      |

## Language Context

- Primary language: Dutch (Nederlands)
- User's native language: Russian/Ukrainian
- Course level: A2 (elementary)
- Provide bilingual support when helpful (Dutch ↔ Russian/English)
