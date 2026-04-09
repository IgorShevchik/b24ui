---
name: bx-translate-locales
description: >-
  Translates the `messages` field of all locale files in src/runtime/locale/
  from a source language to all other languages. Use when asked to translate
  locales, update locale translations, or run bx-translate-locales.
argument-hint: [source-locale]
disable-model-invocation: true
allowed-tools: Read Write Bash
---

# Translate Locale Messages

Translate the `messages` object in every `src/runtime/locale/*.ts` file from a source language to all other locale files.

## CRITICAL CONSTRAINTS

- **YOU are the translator.** Use YOUR OWN language knowledge. You are a multilingual LLM.
- **NEVER** create scripts, temporary files, or call external APIs for translation.
- **NEVER** skip a file. You MUST rewrite EVERY target file with translated values.
- If a string value is `''` (empty), you MUST fill it with a translation.
- If a string value already has text, you MUST replace it with a fresh translation.
- If a key from the source file is **missing** in the target, you MUST add it with a translation.
- The ONLY tools you use: **Read** a file, **Write** the file back with translations.

## Input

Source locale code from user message (e.g. `pl`, `ru`). Default: `en`.

## Workflow

### Step 0: Normalize source

Read `src/runtime/locale/{source-locale}.ts`. Replace all `...` (three ASCII dots) with `…` (U+2026) in message string values. Write back.

### Step 1: Translate targets

List `.ts` files in `src/runtime/locale/` (skip `index.ts` and source). For each target:

1. Read the target file.
2. The target's `messages` must have **the same key structure** as the source. The source file is the reference for the `Messages` type defined in `src/runtime/types/locale.ts`. This means:
   - `''` (empty) → fill with translation
   - `'existing text'` → replace with fresh translation
   - **missing key** → add it with a translated value
   - ALL required keys must be present and non-empty after you finish
3. Keep unchanged: `import` lines, `name`, `code`, `locale`, `dir`, indentation, single quotes.
4. Use `…` (not `...`) in ALL languages.
5. Write the complete file. Report: `Updated {code}.ts`

Process files one at a time.

## Translation Quality

Translate for **real UI users**, not a dictionary. Use natural phrasing a native speaker would use in software.

- Do NOT translate word-for-word. Adapt meaning to sound native.
- Think about what the UI element **communicates to the user**.

Good vs bad (English → Russian):

| Source (en)              | BAD                          | GOOD                                |
| ------------------------ | ---------------------------- | ----------------------------------- |
| `Thinking...`            | `Думает...`                  | `Размышляет…`                       |
| `Thought`                | `Мысль`                      | `Размышление завершено`             |
| `Thought for {duration}` | `Мысль в течение {duration}` | `Размышление заняло {duration}`     |
| `Dark`                   | `Тёмный`                     | `Тёмная` (feminine, matches "тема") |
| `System`                 | `Системный`                  | `Системная`                         |

## Rules

- **Placeholders**: Keep `{slide}`, `{label}`, `{filename}`, `{duration}` unchanged.
- **Do not translate**: `Bitrix24`, `AI`, `CRM`.
- **Special chars**: `...` → `…` in ALL languages. `--` → `—` for ru, ua, kz.

### Typography by language

| Locale(s)  | Notes                                                     |
| ---------- | --------------------------------------------------------- |
| `ru`, `ua` | Ellipsis `…`, em-dash `—`, feminine gender for тема/режим |
| `ar`       | `؟` `،` `؛`                                               |
| `fr`       | Non-breaking space before `?` `!` `:` `;`                 |
| `sc`, `tc` | Fullwidth `。，？！`                                      |
| `ja`       | Fullwidth `。、？！`                                      |
| `de`       | Nouns capitalized                                         |
| `th`       | No spaces between words                                   |

## Example

Source `en.ts` has keys: `alert.close`, `carousel.goto`, `chatPrompt.placeholder`.

Target `pl.ts` BEFORE (empty strings + missing key `chatPrompt`):

```ts
import type { Messages } from '../types'
import { defineLocale } from '../composables/defineLocale'

export default defineLocale<Messages>({
  name: 'Polski',
  code: 'pl',
  locale: 'pl',
  messages: {
    alert: {
      close: ''
    },
    carousel: {
      goto: '',
      next: 'Następny'
    }
  }
})
```

Target `pl.ts` AFTER:

```ts
import type { Messages } from '../types'
import { defineLocale } from '../composables/defineLocale'

export default defineLocale<Messages>({
  name: 'Polski',
  code: 'pl',
  locale: 'pl',
  messages: {
    alert: {
      close: 'Zamknij'
    },
    carousel: {
      goto: 'Przejdź do {slide}',
      next: 'Następny'
    },
    chatPrompt: {
      placeholder: 'Wpisz swoją wiadomość tutaj…'
    }
  }
})
```

What happened: empty `''` filled, existing `'Następny'` re-translated, missing `chatPrompt` block added. Single quotes, no semicolons. Imports/name/code/locale untouched.
