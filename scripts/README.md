# Scripts

Утилиты для автоматизации создания учебных материалов.

---

## audio_to_anki.py

Автоматическая нарезка аудио диалогов на отдельные предложения и генерация
Anki карточек с аутентичной озвучкой.

### Назначение

Превращает учебный аудиофайл (диалог, упражнение) в набор Anki карточек, где
каждое предложение = 1 карточка с оригинальным аудио из учебника.

---

## Быстрый старт

```bash
# Полный цикл: транскрипция → нарезка → копирование в Anki
python3 scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 \
    --theme gezondheid \
    --copy-to-anki
```

После выполнения:

1. Заполни переводы в `sententiae_gezondheid_anki.txt`
2. Импортируй в Anki: File → Import

---

## Зависимости

### Установка (один раз)

```bash
# FFmpeg — нарезка аудио
brew install ffmpeg

# OpenAI Whisper — распознавание речи
pip install openai-whisper
```

### Проверка установки

```bash
ffmpeg -version    # Должна показать версию
whisper --help     # Должна показать справку
```

---

## Как это работает

### Архитектура

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           audio_to_anki.py                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────────────┐ │
│  │  INPUT   │    │  WHISPER  │    │  FFMPEG  │    │     OUTPUT       │ │
│  │  MP3     │───▶│  (ASR)    │───▶│  (split) │───▶│  Anki cards +    │ │
│  │  file    │    │           │    │          │    │  audio segments  │ │
│  └──────────┘    └───────────┘    └──────────┘    └──────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    --copy-to-anki (опционально)                  │  │
│  │  Автоматический поиск Anki media folder + копирование            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Пошаговый процесс

| Шаг | Компонент | Что делает | Результат |
|-----|-----------|------------|-----------|
| 1 | **Whisper** | Распознаёт голландскую речь | JSON с текстом + таймстемпы |
| 2 | **FFmpeg** | Нарезает MP3 по таймстемпам | Отдельные MP3 для каждой фразы |
| 3 | **Генератор** | Создаёт Anki import файл | TSV файл с карточками |
| 4 | **Копирование** | Переносит в Anki media | Аудио готово к использованию |

### Детали реализации

**Whisper:**

- Модель: `base` (оптимально для учебного аудио)
- Язык: Dutch (нидерландский)
- Выход: JSON с сегментами `{start, end, text}`

**FFmpeg:**

- Кодек: libmp3lame (качество 2)
- Padding: -0.1s до начала, +0.2s после конца
- Формат имени: `{prefix}_sentence_{NNN}.mp3`

**Anki файл:**

- Формат: TSV (tab-separated values)
- Поля: Dutch | Russian | Audio | Tags
- Теги: `sententiae::{theme}::{level}::audio`

---

## Параметры командной строки

```bash
python3 scripts/audio_to_anki.py [audio] [options]
```

### Обязательные

| Параметр | Описание | Пример |
|----------|----------|--------|
| `audio` | Путь к MP3 файлу | `thema_7/2/h07_oefening_02.mp3` |

### Опциональные

| Параметр | Описание | По умолчанию | Пример |
|----------|----------|--------------|--------|
| `--theme` | Тема для тегов Anki | `general` | `gezondheid` |
| `--level` | Уровень CEFR | `A2` | `A1`, `B1` |
| `--copy-to-anki` | Копировать аудио в Anki | выключено | флаг |

### Справка

```bash
python3 scripts/audio_to_anki.py --help
```

---

## Выходные файлы

### Структура после выполнения

```
thema_7/2/
├── h07_oefening_02.mp3                    # Исходный файл (не изменяется)
├── h07_oefening_02.json                   # Whisper output
│                                          # (таймстемпы для отладки)
├── h07_oefening_02_sentences/             # Нарезанные аудио
│   ├── h07_oefening_02_sentence_001.mp3   # "Hoi schat, lekker getennist?"
│   ├── h07_oefening_02_sentence_002.mp3   # "Niet echt."
│   ├── h07_oefening_02_sentence_003.mp3   # "Het eerste half uur..."
│   └── ... (по количеству сегментов)
│
└── sententiae_gezondheid_anki.txt         # Anki import файл
```

### Формат Anki файла

```
#separator:tab
#html:true
#tags column:4

Hoi schat, lekker getennist?	[TODO: перевод]	[sound:h07_oefening_02_sentence_001.mp3]	sententiae::gezondheid::A2::audio
Niet echt.	[TODO: перевод]	[sound:h07_oefening_02_sentence_002.mp3]	sententiae::gezondheid::A2::audio
```

### Anki media folder

При использовании `--copy-to-anki` файлы копируются в:

```
~/Library/Application Support/Anki2/{profile}/collection.media/
```

Скрипт автоматически находит профиль:

- Если профиль один — использует его
- Если несколько — использует первый + предупреждение

---

## Примеры использования

### Базовый (без автокопирования)

```bash
python3 scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid
```

Затем вручную:

```bash
cp thema_7/2/h07_oefening_02_sentences/*.mp3 \
   ~/Library/Application\ Support/Anki2/alex/collection.media/
```

### Рекомендуемый (с автокопированием)

```bash
python3 scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 \
    --theme gezondheid \
    --copy-to-anki
```

### Разные темы

```bash
# Thema 7: Gezondheid (здоровье)
python3 scripts/audio_to_anki.py thema_7/2/h07_oefening_02.mp3 --theme gezondheid --copy-to-anki

# Thema 6: Wonen (жильё)
python3 scripts/audio_to_anki.py thema_6/audio.mp3 --theme wonen --copy-to-anki

# Thema 5: Werk (работа), уровень B1
python3 scripts/audio_to_anki.py thema_5/dialog.mp3 --theme werk --level B1 --copy-to-anki
```

---

## Постобработка

### 1. Корректировка текста (опционально)

Whisper модель `base` может ошибаться в:

- Медицинских терминах (`fysiotherapeut` → `visu-terap`)
- Именах собственных (`Notenbomenlaan` → `noot een wonenlaan`)
- Разговорных формах (`schat` → `schap`)

**Решение:** Сравни с оригинальной транскрипцией и исправь в txt файле.

### 2. Добавление переводов

Открой `sententiae_{theme}_anki.txt` и замени `[TODO: перевод]`:

```
Hoi schat, lekker getennist?	Привет, дорогой, хорошо поиграл в теннис?	[sound:...]	...
```

### 3. Импорт в Anki

1. File → Import
2. Выбери `sententiae_{theme}_anki.txt`
3. Настрой поля:
   - Field 1 → Front
   - Field 2 → Back
   - Field 3 → Audio
   - Field 4 → Tags

### 4. Настройка карточки (один раз)

**Tools → Manage Note Types → [твой тип] → Cards**

Front Template:

```html
{{Front}}
{{Audio}}
```

Back Template:

```html
{{FrontSide}}
<hr id=answer>
{{Back}}
```

---

## Troubleshooting

| Проблема | Причина | Решение |
|----------|---------|---------|
| `whisper: command not found` | Whisper не установлен | `pip install openai-whisper` |
| `ffmpeg: command not found` | FFmpeg не установлен | `brew install ffmpeg` |
| Аудио не играет в Anki | Файлы не в media folder | Используй `--copy-to-anki` или скопируй вручную |
| Anki media folder не найден | Anki не запускался | Запусти Anki хотя бы раз |
| Плохое качество распознавания | Модель `base` слишком простая | Измени на `medium` в скрипте (строка ~104) |
| Границы сегментов неточные | Whisper ошибся | Отредактируй `.json` файл вручную |

### Проверка Anki media

В Anki: **Tools → Check Media**

Покажет:

- Отсутствующие файлы (referenced but missing)
- Лишние файлы (in media but unused)

---

## Технические детали

### Поддерживаемые платформы

| ОС | Путь к Anki |
|----|-------------|
| macOS | `~/Library/Application Support/Anki2/` |
| Linux | `~/.local/share/Anki2/` |
| Windows | `%APPDATA%\Anki2\` |

### Whisper модели

| Модель | Размер | Скорость | Качество | Рекомендация |
|--------|--------|----------|----------|--------------|
| `tiny` | 39 MB | Очень быстро | Низкое | Для тестов |
| `base` | 74 MB | Быстро | Хорошее | **По умолчанию** |
| `small` | 244 MB | Средне | Лучше | Если base не справляется |
| `medium` | 769 MB | Медленно | Отличное | Для сложного аудио |
| `large` | 1550 MB | Очень медленно | Лучшее | Для критичных задач |

### Изменение модели

В файле `audio_to_anki.py`, строка ~104:

```python
"--model",
"base",  # Изменить на: small, medium, large
```

---

## Альтернативы

Если Whisper не подходит:

| Инструмент | Плюсы | Минусы |
|------------|-------|--------|
| **Aeneas** | Использует ТВОЮ транскрипцию | Требует подготовки текста |
| **Audacity** | Точный контроль | Долго, ручная работа |
| **Google Speech-to-Text** | Хорошее качество | Платный API |
