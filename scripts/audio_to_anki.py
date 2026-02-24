#!/usr/bin/env python3
"""
Audio to Anki Sentence Cards Generator

Использование:
    python scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid --level A2

С автокопированием в Anki:
    python scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid --copy-to-anki

Что делает:
    1. Транскрибирует MP3 через Whisper (с таймстемпами)
    2. Нарезает аудио на отдельные предложения
    3. Генерирует Anki import файл (переводы добавляются вручную)
    4. Опционально копирует аудио в Anki media folder
"""

import argparse
import json
import subprocess
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from anki_utils import find_anki_media_folder, validate_anki_media, copy_to_anki_media


def transcribe_with_whisper(audio_path: Path, word_timestamps: bool = False) -> dict:
    """
    Запускает Whisper и возвращает JSON с сегментами.

    Args:
        audio_path: путь к MP3 файлу
        word_timestamps: если True, включает word-level timestamps для alignment
    """
    print(f"   Модель: base (оптимально для учебного аудио)")
    if word_timestamps:
        print(f"   Word timestamps: включены (для forced alignment)")

    cmd = [
        "whisper",
        str(audio_path),
        "--language",
        "Dutch",
        "--output_format",
        "json",
        "--output_dir",
        str(audio_path.parent),
        "--model",
        "base",  # base достаточно для чёткой учебной речи
    ]

    if word_timestamps:
        cmd.append("--word_timestamps")
        cmd.append("True")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Ошибка Whisper: {result.stderr}")
        raise RuntimeError("Whisper transcription failed")

    json_path = audio_path.with_suffix(".json")
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def extract_words_from_whisper(whisper_data: dict) -> list[dict]:
    """
    Извлекает слова с таймстампами из Whisper JSON.

    Whisper с word_timestamps=True возвращает слова внутри сегментов:
    segments[].words[] = {"word": "Hoi", "start": 0.0, "end": 0.3}
    """
    words = []

    for segment in whisper_data.get("segments", []):
        segment_words = segment.get("words", [])
        for w in segment_words:
            words.append({
                "word": w.get("word", "").strip(),
                "start": w.get("start", 0),
                "end": w.get("end", 0),
            })

    return words


def find_best_match(
    sentence_words: list[str],
    whisper_words: list[dict],
    start_idx: int = 0,
    similarity_threshold: float = 0.6,
) -> dict | None:
    """
    Находит лучшее совпадение для предложения в потоке слов Whisper.

    Использует скользящее окно + fuzzy matching для устойчивости к ошибкам Whisper.

    Args:
        sentence_words: нормализованные слова предложения из MD
        whisper_words: список слов от Whisper с таймстампами
        start_idx: с какого индекса начинать поиск (оптимизация)
        similarity_threshold: минимальный порог схожести

    Returns:
        {"start": float, "end": float, "match_idx": int} или None
    """
    if not sentence_words or not whisper_words:
        return None

    window_size = len(sentence_words)
    best_match = None
    best_score = similarity_threshold  # Минимальный порог

    # Ограничиваем поиск: не смотрим слишком далеко назад
    search_start = max(0, start_idx - 5)

    for i in range(search_start, len(whisper_words) - window_size + 1):
        # Собираем слова из окна Whisper
        window_words = [
            normalize_text(w["word"]) for w in whisper_words[i : i + window_size]
        ]

        # Сравниваем как строки (более устойчиво к мелким различиям)
        sentence_str = " ".join(sentence_words)
        window_str = " ".join(window_words)

        score = SequenceMatcher(None, sentence_str, window_str).ratio()

        if score > best_score:
            best_score = score
            best_match = {
                "start": whisper_words[i]["start"],
                "end": whisper_words[i + window_size - 1]["end"],
                "match_idx": i + window_size,  # Для следующего поиска
                "score": score,
            }

    return best_match


def align_sentences(
    sentences: list[dict],
    whisper_words: list[dict],
) -> list[dict]:
    """
    Сопоставляет предложения из MD с таймстампами Whisper.

    Алгоритм:
    1. Для каждого предложения нормализуем текст
    2. Ищем лучшее совпадение в потоке слов (скользящее окно)
    3. Берём start первого слова и end последнего

    Args:
        sentences: [{"speaker": str, "text": str}, ...]
        whisper_words: [{"word": str, "start": float, "end": float}, ...]

    Returns:
        [{"speaker": str, "text": str, "start": float, "end": float}, ...]
    """
    aligned = []
    search_idx = 0  # Оптимизация: начинаем поиск с последнего найденного

    for sent in sentences:
        sentence_words = normalize_text(sent["text"]).split()

        if not sentence_words:
            continue

        match = find_best_match(sentence_words, whisper_words, search_idx)

        if match:
            aligned.append({
                "speaker": sent["speaker"],
                "text": sent["text"],  # Оригинальный текст из MD (чистый!)
                "start": match["start"],
                "end": match["end"],
            })
            search_idx = match["match_idx"]
        else:
            # Не нашли совпадение — пропускаем с предупреждением
            print(f"   ⚠️  Не удалось найти: '{sent['text'][:40]}...'")

    return aligned


def split_audio(audio_path: Path, segments: list, output_dir: Path, prefix: str) -> list:
    """Нарезает аудио по сегментам, возвращает список файлов."""
    output_dir.mkdir(exist_ok=True)
    audio_files = []

    for i, seg in enumerate(segments, 1):
        # Сразу добавляем префикс к имени файла
        output_file = output_dir / f"{prefix}_sentence_{i:03d}.mp3"

        # Добавляем небольшой padding для естественного звучания
        start = max(0, seg["start"] - 0.1)
        end = seg["end"] + 0.2

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(audio_path),
                "-ss",
                str(start),
                "-to",
                str(end),
                "-c:a",
                "libmp3lame",  # Перекодируем для чистых границ
                "-q:a",
                "2",  # Высокое качество
                "-y",
                str(output_file),
            ],
            capture_output=True,
        )
        audio_files.append(output_file.name)

    return audio_files


def clean_text(text: str) -> str:
    """Очищает текст от артефактов Whisper."""
    # Убираем лишние пробелы
    text = re.sub(r"\s+", " ", text.strip())
    # Убираем повторяющиеся знаки препинания
    text = re.sub(r"\.{2,}", ".", text)
    return text


def parse_transcript(md_path: Path) -> list[dict]:
    """
    Парсит MD файл с транскрипцией.

    Формат: "Speaker: текст реплики"
    Возвращает: [{"speaker": "Mila", "text": "Hoi schat..."}, ...]
    """
    sentences = []

    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Пропускаем пустые строки и заголовки
            if not line or line.startswith("#"):
                continue

            # Пропускаем ремарки типа (смех), (пауза)
            if line.startswith("(") and line.endswith(")"):
                continue

            # Формат: "Speaker: текст" или "Speaker:текст" (без пробела)
            match = re.match(r"^([A-Za-zА-Яа-яё]+)\s*:\s*(.+)$", line)
            if match:
                speaker = match.group(1)
                text = match.group(2).strip()

                if text:  # Только если есть текст
                    sentences.append({
                        "speaker": speaker,
                        "text": text,
                    })

    return sentences


def normalize_text(text: str) -> str:
    """Нормализует текст для сравнения (lowercase, без пунктуации)."""
    text = text.lower()
    # Убираем пунктуацию, оставляем только буквы и пробелы
    text = re.sub(r"[^\w\s]", "", text)
    # Нормализуем пробелы
    text = re.sub(r"\s+", " ", text.strip())
    return text


def generate_anki_file(
    segments: list,
    audio_files: list,
    output_path: Path,
    theme: str,
    level: str,
    use_aligned_text: bool = False,
):
    """
    Генерирует Anki import файл.

    Args:
        segments: сегменты (Whisper или aligned)
        audio_files: список имён аудио файлов
        output_path: куда сохранить
        theme: тема для тегов
        level: уровень CEFR
        use_aligned_text: если True, текст уже чистый (из MD), не нужен clean_text
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#tags column:4\n\n")

        for seg, audio_file in zip(segments, audio_files):
            # Для aligned сегментов текст уже чистый (из MD файла)
            if use_aligned_text:
                nl_text = seg["text"]
            else:
                nl_text = clean_text(seg["text"])

            # Пропускаем слишком короткие сегменты (шум, вздохи)
            if len(nl_text) < 3:
                continue

            audio_ref = f"[sound:{audio_file}]"
            tags = f"sententiae::{theme}::{level}::audio"

            # Формат: NL | RU (placeholder) | Audio | Tags
            f.write(f"{nl_text}\t[TODO: перевод]\t{audio_ref}\t{tags}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert audio to Anki sentence cards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
    # Только Whisper (старый режим):
    python scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid

    # С forced alignment (рекомендуется):
    python scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 \\
        --transcript thema_7/2/h07_oefening_02.md --theme gezondheid

    # С автокопированием в Anki:
    python scripts/audio_to_anki.py audio.mp3 --transcript trans.md --theme werk --copy-to-anki
        """,
    )
    parser.add_argument("audio", type=Path, help="Путь к MP3 файлу")
    parser.add_argument(
        "--theme", default="general", help="Тема для тегов (например: gezondheid)"
    )
    parser.add_argument("--level", default="A2", help="Уровень CEFR (A1, A2, B1)")
    parser.add_argument(
        "--copy-to-anki",
        action="store_true",
        help="Автоматически копировать аудио в Anki media folder",
    )
    parser.add_argument(
        "--transcript",
        type=Path,
        help="MD файл с транскрипцией (формат: 'Speaker: текст'). Включает forced alignment.",
    )

    args = parser.parse_args()

    audio_path = args.audio.resolve()

    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_path}")
        return 1

    # Валидируем транскрипцию если указана
    transcript_path = None
    if args.transcript:
        transcript_path = args.transcript.resolve()
        if not transcript_path.exists():
            print(f"❌ Транскрипция не найдена: {transcript_path}")
            return 1

    # Валидируем Anki media folder если нужно копирование
    anki_media = None
    if args.copy_to_anki:
        print("🔍 Ищу Anki media folder...")
        anki_media = validate_anki_media(find_anki_media_folder())
        if anki_media is None:
            print("❌ Anki media folder не найден!")
            print("   Проверь что Anki установлен и запускался хотя бы раз.")
            print("   Или скопируй файлы вручную после генерации.")
            return 1
        print(f"   ✅ Найден: {anki_media}")

    # Создаём уникальный префикс из имени файла
    prefix = audio_path.stem  # h07_oefening_02

    output_dir = audio_path.parent / f"{prefix}_sentences"
    anki_file = audio_path.parent / f"sententiae_{args.theme}_anki.txt"

    # Определяем режим работы
    use_alignment = transcript_path is not None

    if use_alignment:
        # ═══════════════════════════════════════════════════════════════════
        # РЕЖИМ FORCED ALIGNMENT: MD + Whisper word-level → точные границы
        # ═══════════════════════════════════════════════════════════════════
        print(f"🎯 Режим: Forced Alignment")
        print(f"   Транскрипция: {transcript_path.name}")

        # 1. Парсим MD файл
        print(f"\n📖 Парсинг транскрипции...")
        sentences = parse_transcript(transcript_path)
        print(f"   Найдено предложений: {len(sentences)}")

        # 2. Транскрибируем с word-level timestamps
        print(f"\n🎧 Транскрибирую {audio_path.name} (word-level)...")
        whisper_data = transcribe_with_whisper(audio_path, word_timestamps=True)

        # 3. Извлекаем слова
        whisper_words = extract_words_from_whisper(whisper_data)
        print(f"   Слов от Whisper: {len(whisper_words)}")

        # 4. Alignment
        print(f"\n🔗 Выравниваю предложения по словам...")
        segments = align_sentences(sentences, whisper_words)
        print(f"   Выровнено: {len(segments)} из {len(sentences)}")

        use_aligned_text = True

    else:
        # ═══════════════════════════════════════════════════════════════════
        # РЕЖИМ WHISPER-ONLY: старое поведение (сегментация по паузам)
        # ═══════════════════════════════════════════════════════════════════
        print(f"🎧 Режим: Whisper-only (сегментация по паузам)")
        print(f"   💡 Совет: добавь --transcript для точных границ предложений")

        print(f"\n🎧 Транскрибирую {audio_path.name}...")
        data = transcribe_with_whisper(audio_path)

        segments = data["segments"]
        print(f"   Найдено сегментов: {len(segments)}")

        use_aligned_text = False

    # Нарезка и генерация (общие для обоих режимов)
    print(f"\n✂️  Нарезаю аудио...")
    audio_files = split_audio(audio_path, segments, output_dir, prefix)
    print(f"   Создано файлов: {len(audio_files)}")

    print(f"\n📝 Генерирую Anki файл...")
    generate_anki_file(
        segments, audio_files, anki_file, args.theme, args.level, use_aligned_text
    )

    # Копируем в Anki если запрошено
    if anki_media:
        print(f"\n📦 Копирую в Anki media...")
        copied = copy_to_anki_media(output_dir, anki_media, prefix)
        print(f"   Скопировано файлов: {copied}")

    print(f"\n✅ Готово!")
    print(f"   Аудио:  {output_dir}/")
    print(f"   Anki:   {anki_file}")
    if anki_media:
        print(f"   Media:  {anki_media}/")

    print(f"\n📌 Следующие шаги:")
    if not anki_media:
        print(f"   1. Скопируй в Anki media folder:")
        print(f"      cp {output_dir}/*.mp3 ~/Library/Application\\ Support/Anki2/User\\ 1/collection.media/")
        print(f"   2. Заполни переводы в {anki_file.name}")
        print(f"   3. Импортируй в Anki")
    else:
        print(f"   1. Заполни переводы в {anki_file.name}")
        print(f"   2. Импортируй в Anki: File → Import")
        print(f"   3. В Anki: Tools → Check Media (опционально)")

    # Показываем превью первых 3 сегментов
    print(f"\n📋 Превью (первые 3 сегмента):")
    for i, seg in enumerate(segments[:3], 1):
        if use_aligned_text:
            text = seg["text"][:60]
        else:
            text = clean_text(seg["text"])[:60]
        print(f"   {i}. [{seg['start']:.1f}s - {seg['end']:.1f}s] {text}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
