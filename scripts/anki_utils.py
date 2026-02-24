#!/usr/bin/env python3
"""
Shared Anki utilities for audio_to_anki.py and text_to_speech.py.

Functions for finding Anki profiles, validating media folders,
and copying audio files into Anki's collection.media directory.
"""

import shutil
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
