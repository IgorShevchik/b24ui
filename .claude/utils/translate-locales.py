#!/usr/bin/env python3
"""
Скрипт для перевода UI-локалей через Claude Code.

Парсит файлы локалей, сохраняет JSON-payload во временный файл,
вызывает навык /bx-translate-locales (который читает файл через Read),
получает переведённый JSON, записывает результат в .ts и запускает eslint.

Использование:
    python .claude/utils/translate-locales.py [source_locale]

source_locale по умолчанию: en
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Optional

# ─── Константы ────────────────────────────────────────────────────────────────

LOCALE_DIR = Path("src/runtime/locale")
DICTIONARY_FILE = Path("src/runtime/dictionary/i18n.ts")
TEMP_DIR = Path(".claude/temp")
LOG_FILE = Path(".claude/log-translate.jsonl")

CONCURRENT_TASKS = 3  # сколько языков переводить одновременно (потоки, не процессы)
CLAUDE_CMD = "claude"  # CLI Claude Code; должен быть в PATH
CHAT_CONTEXT_MARKER = "chat"  # подстрока в ключе сообщения — отдельный контекст для перевода

IGNORED_FILES: set[str] = {
    # Добавьте имена файлов локалей, которые не нужно переводить:
    # "ru.ts",

    "br.ts",
    "de.ts",
    "fr.ts",
    "it.ts",
    # "pl.ts",
    # "ru.ts",
    # "ua.ts",
    "tr.ts",
    "sc.ts",
    "tc.ts",
    "ja.ts",
    "vn.ts",
    "id.ts",
    "ms.ts",
    "th.ts",
    "in.ts",
    "ar.ts",
    # "kz.ts",
    "ko.ts",
    "hi.ts",
    "la.ts",
    # "en.ts",
    "es.ts",
    "pt.ts",
    "ro.ts",
    "sk.ts",
    "sl.ts",
    "sq.ts",
}

# Коды локалей с письмом справа налево — для них в .ts добавляется dir: 'rtl'.
RTL_LOCALES = {"ar", "he", "fa", "ur"}

# Подсказки модели по типографике и языку (попадают в payload навыка перевода).
TYPOGRAPHY_RULES: dict[str, str] = {
    "ru": "Use ellipsis `…` (not `...`), em-dash `—` (not `--`). Feminine gender for тема/режим (Тёмная, Светлая, Системная).",
    "ua": "Use ellipsis `…` (not `...`), em-dash `—` (not `--`). Feminine gender for тема/режим.",
    "kz": "Use ellipsis `…` (not `...`), em-dash `—` (not `--`).",
    "ar": "Arabic punctuation: `؟` (question mark), `،` (comma), `؛` (semicolon). RTL text direction.",
    "fr": "Non-breaking space (U+00A0) before `:` `;` `!` `?`.",
    "sc": "Fullwidth punctuation: `。` `，` `？` `！`",
    "tc": "Fullwidth punctuation: `。` `，` `？` `！`",
    "ja": "Fullwidth punctuation: `。` `、` `？` `！`",
    "de": "Capitalize all nouns.",
    "th": "No spaces between Thai words.",
}

# Потокобезопасный вывод в консоль.
_print_lock = threading.Lock()


def log(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


# ─── Парсинг словаря i18n.ts ─────────────────────────────────────────────────

def parse_i18n_dictionary() -> list[dict[str, str]]:
    """Читает i18n.ts и вытаскивает массив локалей (code, name, file).

    Не исполняет TypeScript — ищет по тексту шаблон вида
    { code: '…', name: '…', file: '…' }.
    """
    content = DICTIONARY_FILE.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(
        r"\{\s*code:\s*'([^']+)',\s*name:\s*'([^']+)',\s*file:\s*'([^']+)'\s*\}",
        content,
    ):
        entries.append({"code": m.group(1), "name": m.group(2), "file": m.group(3)})
    if not entries:
        print("Ошибка: записи contentLocales не найдены в i18n.ts")
        sys.exit(1)
    return entries


# ─── Парсинг JS-объектов ──────────────────────────────────────────────────────

def parse_js_object(text: str) -> dict[str, Any]:
    """Рекурсивно парсит JS object literal в Python dict."""
    result: dict[str, Any] = {}
    text = text.strip()
    # Снимаем внешние фигурные скобки целиком (один уровень за вызов).
    if text.startswith("{"):
        text = text[1:]
    if text.endswith("}"):
        text = text[:-1]

    pos = 0
    length = len(text)

    while pos < length:
        # Пропускаем запятые и пробелы между парами ключ: значение.
        while pos < length and text[pos] in " \t\n\r,":
            pos += 1
        if pos >= length:
            break

        # Ключ — всё от текущей позиции до первого двоеточия (как в JS).
        key_start = pos
        while pos < length and text[pos] != ":":
            pos += 1
        key = text[key_start:pos].strip()
        if not key:
            break
        pos += 1

        while pos < length and text[pos] in " \t\n\r":
            pos += 1
        if pos >= length:
            break

        if text[pos] == "{":
            # Вложенный объект: считаем глубину скобок, не «ломаясь» о строки в кавычках.
            depth = 1
            start = pos
            pos += 1
            while pos < length and depth > 0:
                ch = text[pos]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                elif ch == "'":
                    pos += 1
                    while pos < length and text[pos] != "'":
                        if text[pos] == "\\":
                            pos += 1
                        pos += 1
                pos += 1
            result[key] = parse_js_object(text[start:pos])
        elif text[pos] == "'":
            # Строка в одинарных кавычках; простой escape: \ следующий символ.
            pos += 1
            chars: list[str] = []
            while pos < length and text[pos] != "'":
                if text[pos] == "\\" and pos + 1 < length:
                    pos += 1
                    chars.append(text[pos])
                else:
                    chars.append(text[pos])
                pos += 1
            result[key] = "".join(chars)
            pos += 1

    return result


# ─── Парсинг .ts файлов локалей ──────────────────────────────────────────────

def parse_locale_file(path: Path) -> dict[str, Any]:
    """Разбирает один locale-файл (.ts): метаданные + объект messages.

    Формат ожидается как у defineLocale: name, code, locale, опционально dir, и блок messages.
    """
    content = path.read_text(encoding="utf-8")

    meta: dict[str, Any] = {
        "name": _extract_field(content, "name") or "",
        "code": _extract_field(content, "code") or "",
        "locale": _extract_field(content, "locale") or "",
        "messages": _extract_messages(content),
    }
    dir_val = _extract_field(content, "dir")
    if dir_val:
        meta["dir"] = dir_val
    return meta


def _extract_field(content: str, field: str) -> Optional[str]:
    m = re.search(rf"^\s*{field}:\s*'([^']*)'", content, re.MULTILINE)
    return m.group(1) if m else None


def _extract_messages(content: str) -> dict[str, Any]:
    """Находит объект после `messages:` и парсит его через parse_js_object."""
    idx = content.find("messages:")
    if idx == -1:
        return {}
    brace_idx = content.index("{", idx)
    depth = 1
    pos = brace_idx + 1
    length = len(content)
    # Сканируем символ за символом: скобки считаем, строки в '...' пропускаем целиком.
    while pos < length and depth > 0:
        ch = content[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == "'":
            pos += 1
            while pos < length and content[pos] != "'":
                if content[pos] == "\\":
                    pos += 1
                pos += 1
        pos += 1
    return parse_js_object(content[brace_idx:pos])


# ─── Fix ... → … ─────────────────────────────────────────────────────────────

def fix_source_ellipsis(path: Path) -> bool:
    """Внутри строковых литералов '...' заменяет три точки на символ многоточия ….

    Трогает только содержимое в одинарных кавычках, чтобы не испортить код вне строк.
    Возвращает True, если файл перезаписан.
    """
    content = path.read_text(encoding="utf-8")
    new_content = re.sub(
        r"'[^']*'",
        lambda m: m.group(0).replace("...", "\u2026"),
        content,
    )
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


# ─── Подготовка payload ───────────────────────────────────────────────────────

def detect_chat_context_keys(messages: dict[str, Any]) -> list[str]:
    """Ключи, в имени которых есть «chat» — навыку перевода передаются отдельным списком."""
    return [k for k in messages if CHAT_CONTEXT_MARKER in k.lower()]


def get_typography_rules(locale_code: str) -> str:
    """Текст правил типографики для кода локали или общий дефолт."""
    return TYPOGRAPHY_RULES.get(locale_code, "Use ellipsis `…` (not `...`).")


# ─── Вызов Claude ────────────────────────────────────────────────────────────

def write_temp_payload(locale_code: str, payload: dict[str, Any]) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = TEMP_DIR / f"translate-{locale_code}.json"
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return temp_path


def cleanup_temp(locale_code: str) -> None:
    temp_path = TEMP_DIR / f"translate-{locale_code}.json"
    temp_path.unlink(missing_ok=True)


# ─── Вызов Claude через навык ────────────────────────────────────────────────

def call_claude_translate(temp_path: Path) -> dict[str, Any]:
    """Вызывает навык /bx-translate-locales, передавая путь к temp-файлу.

    Навык использует Read для чтения payload, переводит и возвращает JSON.
    """
    prompt = f"/bx-translate-locales {temp_path}"

    cmd = [
        CLAUDE_CMD, "-p", prompt,
        "--output-format", "json",
        "--tools", "Read",
        "--dangerously-skip-permissions",
    ]
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding="utf-8",
        errors="replace",
    )

    if proc.returncode != 0:
        details = proc.stderr or proc.stdout or "<no output>"
        raise RuntimeError(
            f"claude exit {proc.returncode}:\n{details[:1000]}"
        )

    if not proc.stdout.strip():
        raise RuntimeError("claude вернул пустой stdout")

    outer = json.loads(proc.stdout)

    if outer.get("is_error"):
        raise RuntimeError(f"claude error: {outer.get('result', outer)}")

    result_text = outer.get("result", "")
    return extract_json(result_text)


def extract_json(text: str) -> dict[str, Any]:
    """Достаёт JSON из ответа модели: целиком, из fenced-блока ``` или по первым фигурным скобкам."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Частый случай: модель оборачивает JSON в markdown-код-блок.
    m = re.search(r"```(?:json)?\s*\n(.*?)\n\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Запасной вариант: жадно взять объект от первой { до последней }.
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Не удалось извлечь JSON из ответа:\n{text[:500]}")


# ─── Генерация .ts файлов ────────────────────────────────────────────────────

def serialize_messages(obj: dict[str, Any], indent: int = 4) -> str:
    """Превращает вложенный dict в текст фрагмента JS-объекта (ключи как в исходниках, строки в '...')."""
    lines: list[str] = []
    keys = list(obj.keys())
    for i, key in enumerate(keys):
        value = obj[key]
        is_last = i == len(keys) - 1
        comma = "" if is_last else ","
        pad = " " * indent
        if isinstance(value, dict):
            lines.append(f"{pad}{key}: {{")
            inner = serialize_messages(value, indent + 2)
            if inner:
                lines.append(inner)
            lines.append(f"{pad}}}{comma}")
        else:
            # Экранируем одинарную кавычку внутри строки для валидного JS/TS литерала.
            escaped = str(value).replace("'", "\\'")
            lines.append(f"{pad}{key}: '{escaped}'{comma}")
    return "\n".join(lines)


def generate_ts_content(meta: dict[str, Any], messages: dict[str, Any]) -> str:
    """Собирает полный текст .ts файла локали (импорты + defineLocale(...))."""
    dir_line = f"  dir: '{meta['dir']}',\n" if "dir" in meta else ""
    messages_block = serialize_messages(messages, indent=4)
    return (
        "import type { Messages } from '../types'\n"
        "import { defineLocale } from '../composables/defineLocale'\n"
        "\n"
        "export default defineLocale<Messages>({\n"
        f"  name: '{meta['name']}',\n"
        f"  code: '{meta['code']}',\n"
        f"  locale: '{meta['locale']}',\n"
        f"{dir_line}"
        "  messages: {\n"
        f"{messages_block}\n"
        "  }\n"
        "})\n"
    )


# ─── Обработка одной локали ───────────────────────────────────────────────────

def process_single_target(
    source_locale: str,
    source_messages: dict[str, Any],
    target: dict[str, str],
    chat_keys: list[str],
) -> dict[str, Any]:
    """Один целевой язык: метаданные → Claude → запись файла локали."""
    target_code = target["code"]
    target_file = target["file"]
    target_path = LOCALE_DIR / target_file

    log(f"  >> {target_file} ({target['name']}) — перевод…")

    if target_path.exists():
        # Сохраняем уже прописанные name/code/locale/dir из файла (ручные правки не затираем).
        existing = parse_locale_file(target_path)
        meta = {
            "name": existing["name"],
            "code": existing["code"],
            "locale": existing["locale"],
        }
        if "dir" in existing:
            meta["dir"] = existing["dir"]
    else:
        # Новый файл: берём подписи из словаря i18n; RTL — сразу выставляем направление.
        meta = {
            "name": target["name"],
            "code": target_code,
            "locale": target_code,
        }
        if target_code in RTL_LOCALES:
            meta["dir"] = "rtl"

    # Всё, что нужно навыку перевода: исходные строки, цель, пометки для чата и типографика.
    payload = {
        "source_locale": source_locale,
        "target_locale": target_code,
        "target_name": target["name"],
        "source_messages": source_messages,
        "chat_context_keys": chat_keys,
        "typography_rules": get_typography_rules(target_code),
    }

    temp_path = write_temp_payload(target_code, payload)
    try:
        result = call_claude_translate(temp_path)
        translations = result.get("translations", result)

        content = generate_ts_content(meta, translations)
        target_path.write_text(content, encoding="utf-8")

        return {"file": target_file, "code": target_code, "status": "success"}
    finally:
        cleanup_temp(target_code)


def process_all_targets(
    source_locale: str,
    source_messages: dict[str, Any],
    targets: list[dict[str, str]],
    chat_keys: list[str],
) -> list[dict[str, Any]]:
    """Переводит все целевые локали с ограничением параллелизма (очередь задач в пуле потоков)."""
    results: list[dict[str, Any]] = []
    total = len(targets)
    completed = 0

    with ThreadPoolExecutor(max_workers=CONCURRENT_TASKS) as executor:
        # Каждая future сопоставлена записи словаря — удобно печатать код/имя при завершении.
        future_to_target = {
            executor.submit(
                process_single_target, source_locale, source_messages, t, chat_keys
            ): t
            for t in targets
        }
        for future in as_completed(future_to_target):
            completed += 1
            target = future_to_target[future]
            try:
                result = future.result()
                results.append(result)
                log(
                    f"  [{completed}/{total}] "
                    f"{target['file']} ({target['name']}) — OK"
                )
            except Exception as e:
                results.append({
                    "file": target["file"],
                    "code": target["code"],
                    "status": "error",
                    "error": str(e),
                })
                log(
                    f"  [{completed}/{total}] "
                    f"{target['file']} ({target['name']}) — ОШИБКА: {e}"
                )

    return results


# ─── ESLint ───────────────────────────────────────────────────────────────────

def run_eslint() -> None:
    """Форматирует и правит стиль .ts в папке локалей через eslint --fix."""
    result = subprocess.run(
        ["npx", "eslint", "--fix", f"{LOCALE_DIR}/"],
        capture_output=True,
        text=True,
    )
    # Ненулевой код у eslint часто бывает при предупреждениях — печатаем хвост stderr.
    if result.returncode != 0 and result.stderr:
        print(f"   ESLint warnings:\n{result.stderr[:500]}")
    else:
        print("   ESLint OK")


# ─── Проверка соответствия ────────────────────────────────────────────────────

def check_consistency(locales: list[dict[str, str]]) -> None:
    """Предупреждения: файл из i18n отсутствует на диске или на диске есть лишний .ts."""
    for loc in locales:
        fpath = LOCALE_DIR / loc["file"]
        if not fpath.exists():
            print(f"   WARNING: {loc['file']} из i18n.ts не найден в {LOCALE_DIR}")

    # Обратная проверка: лишние .ts в папке (кроме index.ts), не прописанные в словаре.
    dict_files = {entry["file"] for entry in locales}
    for fpath in LOCALE_DIR.glob("*.ts"):
        if fpath.name == "index.ts":
            continue
        if fpath.name not in dict_files:
            print(f"   WARNING: {fpath.name} в {LOCALE_DIR} не указан в i18n.ts")


# ─── Лог ──────────────────────────────────────────────────────────────────────

def save_log(results: list[dict[str, Any]]) -> None:
    """Дописывает в JSONL по одной строке JSON на каждую обработанную локаль."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Точка входа: оркестрация шагов 1–6 и вывод прогресса в консоль."""
    # Аргумент командной строки — код исходной локали (файл строк для перевода).
    source_locale = sys.argv[1] if len(sys.argv) > 1 else "en"
    print(f"Исходная локаль: {source_locale}")

    print("\n1. Чтение словаря i18n.ts\u2026")
    locales = parse_i18n_dictionary()
    print(f"   Найдено локалей: {len(locales)}")

    source_entry = next((l for l in locales if l["code"] == source_locale), None)
    if not source_entry:
        print(f"Ошибка: локаль '{source_locale}' не найдена в словаре")
        sys.exit(1)

    # Все языки из словаря, кроме исходного и явно игнорируемых файлов.
    targets = [
        l for l in locales
        if l["code"] != source_locale and l["file"] not in IGNORED_FILES
    ]
    ignored = [l for l in locales if l["file"] in IGNORED_FILES]
    if ignored:
        print(f"   Игнорируются: {', '.join(l['code'] for l in ignored)}")
    print(f"   Целевые локали ({len(targets)}): "
          + ", ".join(t["file"] for t in targets))

    source_path = LOCALE_DIR / source_entry["file"]
    if not source_path.exists():
        print(f"Ошибка: файл {source_path} не найден")
        sys.exit(1)

    print(f"\n2. Чтение {source_path}\u2026")
    if fix_source_ellipsis(source_path):
        print("   Исправлены '...' \u2192 '\u2026' в source-файле")

    source_data = parse_locale_file(source_path)
    source_messages = source_data["messages"]

    # Ключи «чатовых» строк передаются в payload отдельно (контекст для корректного тона).
    chat_keys = detect_chat_context_keys(source_messages)
    if chat_keys:
        print(f"   Chat-контекст: {', '.join(chat_keys)}")

    print(f"\n3. Перевод (до {CONCURRENT_TASKS} параллельно)\u2026")
    results = process_all_targets(source_locale, source_messages, targets, chat_keys)

    # Приводим сгенерированные файлы к стилю проекта (отступы, кавычки и т.д.).
    print("\n4. Запуск eslint --fix\u2026")
    run_eslint()

    success = sum(1 for r in results if r["status"] == "success")
    errors = len(results) - success
    print(f"\n5. Итого: успешно {success}, ошибок {errors}")

    if errors:
        print("\n   Ошибки:")
        for r in results:
            if r["status"] == "error":
                print(f"     {r['file']}: {r['error']}")

    # Только предупреждения; не останавливает скрипт.
    print("\n6. Проверка соответствия\u2026")
    check_consistency(locales)

    # Аудит: каждый прогон дописывается в конец log-translate.jsonl.
    save_log(results)
    print(f"\nГотово. Лог: {LOG_FILE}")

    # Подчищаем temp-папку если пуста.
    if TEMP_DIR.exists() and not any(TEMP_DIR.iterdir()):
        TEMP_DIR.rmdir()


if __name__ == "__main__":
    main()
