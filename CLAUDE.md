# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Purpose

This is a Dutch language learning materials directory for the "De Opmaat" course
(NT2 - Nederlands als Tweede Taal, targeting A2 level). It contains vocabulary
lists, tests, audio files, Anki flashcard materials, and supplementary
documents.

## Directory Structure

- `thema_1/` through `thema_4/` - Course materials organized by theme/chapter
- `existin_not_sorted/` - Raw/unsorted learning materials and vocabulary exports
- `other/` - Administrative documents (registration forms, payment receipts)
- Root contains supplementary materials (e.g., verb conjugation lists)

## Common File Types

- `.pdf` - Vocabulary lists (woordenlijst), tests (toetsen), answer keys
  (beoordeling)
- `.mp3` - Audio exercises and listening materials
- `.docx` - Word documents for forms and reference materials
- `.md` - Converted tests and grammar notes for interactive practice
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

## Common Tasks

### PDF to Markdown Conversion

Convert PDF tests to editable markdown for interactive practice sessions. Output
should preserve exercise structure with blank answer spaces.

### Interactive Dutch Practice

- Review and correct user's Dutch sentences
- Provide grammar explanations when corrections are needed
- Track common spelling mistakes to reinforce learning

### Working with Anki Files

- When creating new word lists, maintain the Anki format conventions
- Dutch nouns should include articles (de/het)
- Keep thematic organization when adding new content
- Dialogues can exist in plain text and audio-referenced versions

### Grammar Explanations

When explaining Dutch grammar, use tables to show word order patterns:

- **want** → normal word order (subject + verb)
- **omdat/als** → verb to the end
- **inversie** → when sentence starts with non-subject element

### Spelling Corrections

Common mistakes to watch for:

- kapot (not capot)
- stropdas (not stroopdas)
- het station (het-woord, not de)

## Language Context

- Primary language: Dutch (Nederlands)
- User's native language: Russian/Ukrainian
- Course level: A2 (elementary)
- Provide bilingual support when helpful (Dutch ↔ Russian/English)
- How to generate stories and postactions: What's included:
  - The story text with bolded verbs for easy pattern recognition
  - Grammar summary tables showing each pattern
  - Vocabulary list (Dutch → Russian → English)

  Would you like me to:
  1. Create more stories with different themes (shopping, daily routine)?
  2. Add audio script markers for ElevenLabs TTS?
  3. Create an Anki-compatible version of the story sentences?
