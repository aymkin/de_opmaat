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
import shutil
import subprocess
import re
import sys
from pathlib import Path

# Базовые пути к Anki2 (кроссплатформенно)
ANKI_BASE_PATHS = [
    Path.home() / "Library/Application Support/Anki2",  # macOS
    Path.home() / ".local/share/Anki2",  # Linux
    Path.home() / "AppData/Roaming/Anki2",  # Windows
]

# Системные папки Anki (не профили)
ANKI_SYSTEM_DIRS = {"addons21", "logs", "crash_reports"}


def find_anki_profiles(base_path: Path) -> list[Path]:
    """Находит все профили пользователей в директории Anki2."""
    profiles = []

    if not base_path.exists():
        return profiles

    for item in base_path.iterdir():
        # Пропускаем системные папки и файлы
        if not item.is_dir() or item.name in ANKI_SYSTEM_DIRS:
            continue

        # Профиль — это папка с collection.media внутри
        media_dir = item / "collection.media"
        if media_dir.exists():
            profiles.append(media_dir)

    return profiles


def find_anki_media_folder() -> Path | None:
    """
    Ищет Anki media folder на текущей машине.
    Если профиль один — использует его автоматически.
    """
    for base_path in ANKI_BASE_PATHS:
        profiles = find_anki_profiles(base_path)

        if len(profiles) == 1:
            # Один профиль — используем его
            return profiles[0]
        elif len(profiles) > 1:
            # Несколько профилей — используем первый, но предупреждаем
            print(f"   ⚠️  Найдено {len(profiles)} профилей, использую: {profiles[0].parent.name}")
            return profiles[0]

    return None


def validate_anki_media(media_path: Path | None) -> Path | None:
    """Валидирует путь к Anki media folder."""
    if media_path is None:
        return None

    if not media_path.exists():
        return None

    if not media_path.is_dir():
        return None

    # Проверяем что это похоже на Anki media (можно писать файлы)
    try:
        test_file = media_path / ".write_test"
        test_file.touch()
        test_file.unlink()
        return media_path
    except PermissionError:
        return None


def copy_to_anki_media(source_dir: Path, media_path: Path, prefix: str) -> int:
    """Копирует аудио файлы в Anki media folder."""
    copied = 0
    for audio_file in source_dir.glob("*.mp3"):
        # Файлы уже имеют префикс: h07_oefening_02_sentence_001.mp3
        dest_file = media_path / audio_file.name
        shutil.copy2(audio_file, dest_file)
        copied += 1
    return copied


def transcribe_with_whisper(audio_path: Path) -> dict:
    """Запускает Whisper и возвращает JSON с сегментами."""
    print(f"   Модель: base (оптимально для учебного аудио)")

    result = subprocess.run(
        [
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
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"❌ Ошибка Whisper: {result.stderr}")
        raise RuntimeError("Whisper transcription failed")

    json_path = audio_path.with_suffix(".json")
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


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


def generate_anki_file(
    segments: list,
    audio_files: list,
    output_path: Path,
    theme: str,
    level: str,
):
    """Генерирует Anki import файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write("#tags column:4\n\n")

        for seg, audio_file in zip(segments, audio_files):
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
    python scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid
    python scripts/audio_to_anki.py thema_6/06_02.mp3 --theme wonen --level A2
    python scripts/audio_to_anki.py audio.mp3 --theme werk --copy-to-anki
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

    args = parser.parse_args()

    audio_path = args.audio.resolve()

    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_path}")
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

    print(f"🎧 Транскрибирую {audio_path.name}...")
    data = transcribe_with_whisper(audio_path)

    segments = data["segments"]
    print(f"   Найдено сегментов: {len(segments)}")

    print(f"✂️  Нарезаю аудио...")
    audio_files = split_audio(audio_path, segments, output_dir, prefix)
    print(f"   Создано файлов: {len(audio_files)}")

    print(f"📝 Генерирую Anki файл...")
    generate_anki_file(segments, audio_files, anki_file, args.theme, args.level)

    # Копируем в Anki если запрошено
    if anki_media:
        print(f"📦 Копирую в Anki media...")
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
        text = clean_text(seg["text"])[:60]
        print(f"   {i}. [{seg['start']:.1f}s - {seg['end']:.1f}s] {text}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
