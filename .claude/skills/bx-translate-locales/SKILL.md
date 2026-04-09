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

- **YOU are the translator.** Use your own language knowledge to translate strings directly. You are a multilingual LLM.
- **NEVER** create scripts (.js, .mjs, .cjs, .ts, .py, .sh, or any other executable files).
- **NEVER** call external translation APIs (Google Translate, DeepL, LibreTranslate, MyMemory, or any other service).
- **NEVER** create temporary files, intermediate files, cache directories, or helper utilities.
- **NEVER** use `curl`, `fetch`, or any HTTP requests for translation purposes.
- The ONLY operations you perform are: **Read** a `.ts` file, translate string values in your head, **Write** the updated `.ts` file back.

## Input

The user may provide a **source locale code** (e.g. `pl`, `ru`).
If no code is provided, default to `en`.

## Workflow

1. **Validate** that `src/runtime/locale/{source}.ts` exists by reading it.
2. **List** all `.ts` files in `src/runtime/locale/` (skip `index.ts` and the source file).
3. **For each target file** (e.g. `de.ts`), do exactly this:
   a. Read `src/runtime/locale/de.ts` as plain text.
   b. Translate every string value inside the `messages: { ... }` block from the source language into the target language. Use YOUR OWN language abilities.
   c. Keep everything else in the file unchanged: `import` lines, `name`, `code`, `locale`, `dir`, formatting, indentation, single quotes.
   d. Write the complete updated file back to `src/runtime/locale/de.ts`.
   e. Report: `Updated de.ts`
4. Move to the next file. Process locales **one at a time**.

## Translation Rules

### Placeholders

Keep all placeholders unchanged: `{slide}`, `{label}`, `{filename}`, `{duration}`, `{0}`, etc.

### Key hierarchy

The `messages` object structure (nested keys) must be **identical** to the source. Never add, remove, or rename keys.

### Do not translate

Proper nouns and abbreviations: `Bitrix24`, `AI`, `CRM`.

### Punctuation and typography by language

Each target language has its own typographic conventions. Apply them consistently:

| Locale(s)  | Ellipsis | Quotes       | Notes                                                          |
| ---------- | -------- | ------------ | -------------------------------------------------------------- |
| `ru`, `ua` | `…`      | `«»` or `""` | Use em-dash `—` where appropriate                              |
| `ar`       | `…`      | `""`         | Question mark `؟`, comma `،`, semicolon `؛`                    |
| `fr`       | `…`      | `« »`        | Non-breaking space before `?` `!` `:` `;`                      |
| `sc`, `tc` | `…`      | `""`         | Fullwidth punctuation `。，？！`, no spaces between characters |
| `ja`       | `…`      | `「」`       | Fullwidth `。、？！`                                           |
| `de`       | `…`      | `„"`         | Standard German punctuation                                    |
| `pl`       | `…`      | `„"`         | Standard Polish punctuation                                    |
| `br`       | `…`      | `""`         | Brazilian Portuguese punctuation                               |
| `th`       | `…`      | `""`         | Thai has no spaces between words                               |
| `tr`       | `…`      | `""`         | Standard Turkish punctuation                                   |
| `kz`       | `…`      | `«»`         | Kazakh, similar to Russian conventions                         |
| Other      | `…`      | `""`         | Follow standard conventions of the language                    |

### Formatting consistency

- If the source string ends with `...`, use the proper ellipsis character `…` in the target.
- If the source string ends with `…`, keep `…` in the target.
- Match capitalization rules of the target language (e.g. German nouns are capitalized).

## Full file example

You read `src/runtime/locale/de.ts` and get:

```ts
import type { Messages } from "../types";
import { defineLocale } from "../composables/defineLocale";

export default defineLocale<Messages>({
  name: "Deutsch",
  code: "de",
  locale: "de",
  messages: {
    alert: {
      close: "OLD VALUE",
    },
    carousel: {
      goto: "OLD {slide}",
      next: "OLD",
    },
  },
});
```

Source `en.ts` has `alert.close = 'Close'`, `carousel.goto = 'Go to {slide}'`, `carousel.next = 'Next'`.

You write back the **entire file** with only string values in `messages` replaced:

```ts
import type { Messages } from "../types";
import { defineLocale } from "../composables/defineLocale";

export default defineLocale<Messages>({
  name: "Deutsch",
  code: "de",
  locale: "de",
  messages: {
    alert: {
      close: "Schließen",
    },
    carousel: {
      goto: "Gehe zu {slide}",
      next: "Weiter",
    },
  },
});
```

Notice: `name`, `code`, `locale`, imports — untouched. Only message string values changed.
