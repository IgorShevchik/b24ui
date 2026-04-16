---
name: bx-translate-locales
description: >-
  Translates UI locale strings. Reads a JSON payload from a temp file,
  translates all message values preserving key order, and outputs
  a JSON object with translations. Called by translate-locales.py.
argument-hint: <path-to-payload-json>
disable-model-invocation: true
allowed-tools: Read
---

# Translate Locale Messages

You receive a **file path** as the argument. Your job:

1. **Read** the file at that path using the Read tool.
2. **Parse** the JSON payload inside.
3. **Translate** all string values in `source_messages`.
4. **Output ONLY** a valid JSON object — no markdown, no explanation, no code fences.

## CRITICAL CONSTRAINTS

- **YOU are the translator.** Use YOUR OWN multilingual knowledge. You are a multilingual LLM.
- **NEVER** create files, scripts, or call external APIs.
## Input (JSON file)

```json
{
  "source_locale": "en",
  "target_locale": "ru",
  "target_name": "Русский",
  "source_messages": {
    "alert": { "close": "Close" },
    "chatPrompt": { "placeholder": "Enter your message here..." }
  },
  "chat_context_keys": ["chatPrompt", "chatReasoning"],
  "typography_rules": "language-specific typography rules"
}
```

## Output (your response — raw JSON, nothing else)

```json
{
  "translations": {
    "alert": { "close": "Закрыть" },
    "chatPrompt": { "placeholder": "Введите ваше сообщение здесь…" }
  }
}
```

`translations` MUST have the **exact same key structure and key order** as `source_messages`. Every key present in the source MUST be present with a translated value.

## Translation Quality

These are **UI strings for a web application**: button labels, tooltips, navigation items, modal titles, form placeholders, search prompts, status messages, and notifications. Translate them the way a **native-speaking user expects to see in a polished software interface**.

Guidelines:

- **Do NOT translate word-for-word.** Adapt meaning to sound native in the target language.
- **Use imperative mood for actions**: button text like "Close" should be a verb command ("Закрыть"), not a noun ("Закрытие").
- **Use conventional software terminology**: "Search" in a placeholder translates as the noun form used in apps ("Поиск", not "Искать"; "搜索", not "查找").
- **Think about UI element purpose**: "System" in a theme selector refers to system theme — use the adjective that agrees with the implied noun ("тема" → "Системная", not "Системный").
- **Keep translations concise** — UI space is limited.

### Semantic context from key names

Use parent key names and sibling key names as semantic context when translating ambiguous values. For example, if the parent key is `chatReasoning` and sibling keys are `thinking` / `thought` / `thoughtFor`, infer that `'Thought'` means "reasoning completed", not the noun "a thought".

### Chat context (AI-agent)

**All keys whose name starts with `chat`** (e.g., `chatPrompt`, `chatReasoning`, `chatPromptSubmit`) belong to the **AI‑agent chat interface**. Additionally, keys listed in `chat_context_keys` are also treated as AI‑agent context.

Translate all such keys as if the dialog is from an AI assistant's perspective:

- **AI is the actor** – use third‑person verbs for actions the AI performs (thinking, sending, reasoning).
- **User‑facing prompts** – translate placeholders as natural input prompts for conversing with an AI.
- **Reasoning process** – treat `thinking` as an ongoing process, `thought` as completed reasoning (not a noun “a thought”).
- **Time expressions** – `for {duration}` means “took {duration}” (duration of the AI’s thinking), not “for {duration}”.

**Examples:**
- `"Thinking..."` → `"Размышляет…"` (ru), `"Myśli…"` (pl), `"Думає…"` (ua) – AI is currently thinking.
- `"Thought"` → `"Размышление завершено"` (ru), `"Myślenie zakończone"` (pl), `"Подумав"` (ua) – AI has finished reasoning.
- `"Thought for {duration}"` → `"Размышление заняло {duration}"` (ru), `"Myślenie zajęło {duration}"` (pl), `"Думав {duration}"` (ua) – thinking took that duration.
- `"Enter your message here..."` (chatPrompt) → natural placeholder for talking to an AI.

### Reference translations

| Source (en) | ru | ar | sc | pl | ua | de | fr | es | it |
|---|---|---|---|---|---|---|---|---|---|
| `Close` | `Закрыть` | `إغلاق` | `关闭` | `Zamknij` | `Закрити` | `Schließen` | `Fermer` | `Cerrar` | `Chiudi` |
| `Search…` | `Поиск…` | `بحث…` | `搜索…` | `Szukaj…` | `Пошук…` | `Suchen…` | `Rechercher…` | `Buscar…` | `Cerca…` |
| `No matches found` | `Совпадений не найдено` | `لم يتم العثور على نتائج` | `未找到匹配项` | `Nie znaleziono pasujących wyników` | `Збігів не знайдено` | `Keine Übereinstimmungen gefunden` | `Aucun résultat trouvé` | `No se encontraron coincidencias` | `Nessun risultato trovato` |
| `Switch to dark mode` | `Переключить на тёмную тему` | `التبديل إلى الوضع الداكن` | `切换到深色模式` | `Przełącz na tryb ciemny` | `Перемкнути на темну тему` | `Zu Dunkelmodus wechseln` | `Passer au mode sombre` | `Cambiar a modo oscuro` | `Passa alla modalità scura` |
| `Thinking…` | `Размышляет…` | `يفكر…` | `思考中…` | `Myśli…` | `Думає…` | `Denkt…` | `Réfléchit…` | `Pensando…` | `Sta pensando…` |
| `Thought` | `Размышление завершено` | `تم التفكير` | `思考完成` | `Myślenie zakończone` | `Подумав` | `Gedankengang beendet` | `Réflexion terminée` | `Razonamiento completado` | `Ragionamento completato` |
| `Thought for {duration}` | `Размышление заняло {duration}` | `استغرق التفكير {duration}` | `思考用时 {duration}` | `Myślenie zajęło {duration}` | `Думав {duration}` | `Denkvorgang dauerte {duration}` | `Réflexion a pris {duration}` | `El razonamiento tardó {duration}` | `Il ragionamento ha impiegato {duration}` |

**For Slavic languages (ru, ua, pl, etc.):**
- Use **perfective aspect** (завершённое действие) for `thought` – e.g., `Подумав` (UA), `Pomyślał` (PL).
- `thinking` should be **imperfective, third‑person, present tense** – e.g., `Думає` (UA), `Myśli` (PL).

## Rules

- **Placeholders**: Keep `{slide}`, `{label}`, `{filename}`, `{duration}` unchanged.
- **Do not translate**: `Bitrix24`, `AI`, `CRM`.
- `...` → `…` in ALL languages. `--` → `—` for ru, ua, kz.
- Apply typography from the `typography_rules` field:

| Locale(s) | Rules |
|---|---|
| `ru`, `ua` | Ellipsis `…`, em-dash `—`, feminine gender for тема/режим |
| `kz` | Ellipsis `…`, em-dash `—` |
| `ar` | Arabic punctuation: `؟` `،` `؛` |
| `fr` | Non-breaking space before `?` `!` `:` `;` |
| `sc`, `tc` | Fullwidth: `。，？！` |
| `ja` | Fullwidth: `。、？！` |
| `de` | Nouns capitalized |
| `th` | No spaces between words |
