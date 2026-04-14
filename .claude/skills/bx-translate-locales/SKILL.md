---
name: bx-translate-locales
description: >-
  Translates the `messages` field of all locale files in src/runtime/locale/
  from a source language to all other languages listed in the i18n dictionary.
  Use when asked to translate locales, update locale translations, or run
  bx-translate-locales.
argument-hint: [source-locale]
disable-model-invocation: true
allowed-tools: Read Write Bash Shell Task
---

# Translate Locale Messages

Translate the `messages` object in every locale file listed in `src/runtime/dictionary/i18n.ts` from a source language to all other locales.

## CRITICAL CONSTRAINTS

- **YOU are the translator.** Use YOUR OWN language knowledge. You are a multilingual LLM.
- **NEVER** create scripts, temporary files, or call external APIs for translation.
- **NEVER** skip a file. You MUST rewrite EVERY target file with translated values.
- If a string value is `''` (empty), you MUST fill it with a translation.
- If a string value already has text, you MUST replace it with a fresh translation.
- If a key from the source file is **missing** in the target, you MUST add it with a translation.
- The tools you use: **Read**, **Write**, **Task** (subagents), **Shell** (ESLint).

## Input

Source locale code from user message (e.g. `pl`, `ru`). Default: `en`.

## Workflow

### Step 0: Read dictionary and normalize source

1. Read `src/runtime/dictionary/i18n.ts`. Extract the `contentLocales` array — it is the **single source of truth** for which languages exist. Each entry has `code`, `name`, and `file`.
2. Build the target list: all entries from `contentLocales` except the one matching the source locale code.
3. Read `src/runtime/locale/{source-locale}.ts`. Replace all `...` (three ASCII dots) with `…` (U+2026) in message string values. Write back.

### Step 1: Translate via parallel subagents

Group target locales into **3 subagents** by language family and launch them **in parallel** via the Task tool. This keeps each subagent's context small enough to avoid token limits.

**Subagent groups:**

| Group | Locales | Rationale |
|-------|---------|-----------|
| 1 | `ru`, `ua`, `kz`, `de`, `fr`, `it`, `pl`, `la`, `br` | Cyrillic + Latin-European |
| 2 | `sc`, `tc`, `ja`, `ar`, `tr`, `in` | CJK + Middle East + South Asian |
| 3 | `vn`, `id`, `ms`, `th` | Southeast Asian languages |

If a target locale from `contentLocales` is **not** listed in any row above, assign it to the group whose rationale best matches its script and linguistic family (e.g. Korean `ko` → Group 2 with CJK). If it fits none of the three, add it to Group 3.

If the source locale belongs to one of these groups, omit it from that group. If a group becomes empty, skip it.

**Each subagent prompt MUST include:**

- The **path** to the source file (`src/runtime/locale/{source}.ts`) — the subagent reads it itself
- The list of target locales (code + file) assigned to this group
- The Translation Quality guidelines (compact summary, not full copy)
- The Typography rules **only for this group's languages**
- The file format rules (imports, `defineLocale`, single quotes, no semicolons)

**IMPORTANT: Do NOT embed the full source file content in the subagent prompt.** Instead, instruct the subagent to Read `src/runtime/locale/{source}.ts` as its first action. This dramatically reduces prompt size.

**Each subagent performs:**

1. Read the source file + all assigned target files (parallel batch).
2. For each target file, produce a translated `messages` object following the rules below.
3. Write all translated files (parallel batch).
4. Return a report listing each updated file: `Updated {code}.ts`

### Step 2: Lint fix

After ALL subagents complete, run ESLint auto-fix **only** on locale files:

```bash
npx eslint --fix src/runtime/locale/
```

Report any remaining errors.

### Step 3: Final report

1. Collect reports from all subagents. List every updated file.
2. **Check for mismatches** between the dictionary and the filesystem:
   - For each entry in `contentLocales`: if `src/runtime/locale/{file}` does not exist on disk, print: `WARNING: File {file} from i18n.ts dictionary not found in src/runtime/locale/`
   - For each `.ts` file in `src/runtime/locale/` (excluding `index.ts` and source): if it is not listed in `contentLocales`, print: `WARNING: File {file} exists in src/runtime/locale/ but is not listed in i18n.ts dictionary`

## Translation rules per target file

1. The target's `messages` must have **the same key structure** as the source. The source file is the reference for the `Messages` type defined in `src/runtime/types/locale.ts`. This means:
   - `''` (empty) → fill with translation
   - `'existing text'` → replace with fresh translation
   - **missing key** → add it with a translated value
   - ALL required keys must be present and non-empty after you finish
2. Keep unchanged: `import` lines, `name`, `code`, `locale`, `dir`, indentation, single quotes.
3. Use `…` (not `...`) in ALL languages.
4. Write the complete file.

## Translation Quality

These are **UI strings for a web application**: button labels, tooltips, navigation items, modal titles, form placeholders, search prompts, status messages, and notifications. Translate them the way a **native-speaking user expects to see in a polished software interface**.

Guidelines:

- **Do NOT translate word-for-word.** Adapt meaning to sound native in the target language.
- **Use imperative mood for actions**: button text like "Close" should be a verb command ("Закрыть"), not a noun ("Закрытие").
- **Use conventional software terminology**: "Search" in an input placeholder translates as the noun form used in apps ("Поиск", not "Искать"; "搜索", not "查找").
- **Think about the UI element's purpose**: a "System" option in a theme selector refers to system theme — use the adjective that agrees with the implied noun ("тема" → "Системная", not "Системный").
- **Keep translations concise** — UI space is limited. Avoid verbose constructions when a shorter idiomatic form exists.

### Semantic context from key names

Use **parent and sibling key names** to disambiguate meaning when translating. Keys often encode UI state machines, component roles, or domain context that the English string value alone does not convey.

1. **Parent key = component/feature context.** If the parent is `chatReasoning`, values belong to an AI reasoning indicator, not a generic "thought" concept.
2. **Sibling keys = state relationships.** If sibling keys form a progression (e.g. `thinking` → `thought` → `thoughtFor`), translate them as related states (active → completed → completed with duration), not as isolated words.
3. **Key name vs value mismatch = intent signal.** If a key is named `clear` but the value is `'Try again'`, the value is the user-facing text — translate the value, not the key name.

When in doubt, prefer the interpretation that makes sense as a **UI state or action label** over a literal dictionary translation.

Reference examples across key languages:

| Source (en) | ru | ar | sc |
|-------------|-----|-----|-----|
| `Close` | `Закрыть` | `إغلاق` | `关闭` |
| `Search…` | `Поиск…` | `بحث…` | `搜索…` |
| `No matches found` | `Совпадений не найдено` | `لم يتم العثور على نتائج` | `未找到匹配项` |
| `Switch to dark mode` | `Переключить на тёмную тему` | `التبديل إلى الوضع الداكن` | `切换到深色模式` |
| `Thinking…` | `Размышляет…` | `يفكر…` | `思考中…` |
| `Thought for {duration}` | `Размышление заняло {duration}` | `فكّر لمدة {duration}` | `思考用时 {duration}` |

## Rules

- **Placeholders**: Keep `{slide}`, `{label}`, `{filename}`, `{duration}` unchanged.
- **Do not translate**: `Bitrix24`, `AI`, `CRM`.
- **Special chars**: `...` → `…` in ALL languages. `--` → `—` for ru, ua, kz.

### Typography by language

| Locale(s) | Notes |
|-----------|-------|
| `ru`, `ua` | Ellipsis `…`, em-dash `—`, feminine gender for тема/режим |
| `kz` | Ellipsis `…`, em-dash `—` |
| `ar` | Arabic punctuation: `؟` `،` `؛` |
| `fr` | Non-breaking space before `?` `!` `:` `;` |
| `sc`, `tc` | Fullwidth punctuation: `。，？！` |
| `ja` | Fullwidth punctuation: `。、？！` |
| `de` | Nouns capitalized |
| `th` | No spaces between words |

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
