# AGENTS.md

Self-contained static web game: no build, install, tests, or dependencies. Open `index.html` directly in a browser; its only network request is the Google Fonts `@import` (Huninn / Noto Sans HK).

## Files
- `index.html` — markup, inline `<style>`, and inline game logic. Runtime behavior lives here and it is the GitHub Pages entry point.
- `verb-data.js` — `window.VERB_DATA` dataset, loaded via `<script src>`. Sole copy of the dataset.
- `prompt.md` — LLM prompt that was used to generate the dataset (provenance only, not loaded at runtime).
- `confetti-doodles.svg` — original (purple) source background artwork, purple was the original from the svgrepo or somewhere. provenance only, not loaded at runtime.
- `confetti-doodles-light.svg` / `confetti-doodles-dark.svg` — theme-toned derivatives of `confetti-doodles.svg` (same geometry; fills set to the app's OKLCH theme tokens). Loaded as the `body` background-image, switched by `:root[data-theme="dark"]`.
- `README.md` — project overview.

## Data editing (gotcha)
- The dataset lives only in `verb-data.js` (`window.VERB_DATA = {...};`); edit it directly and keep it valid JS.
- Keep the file self-contained: no network requests, no dependencies.

## Data model (do not violate)
- Each verb: `infinitive`, `translation_zh`/`translation_en`, `notes`, `phrases`.
- `phrases` maps a tense key (one of the 8 in `TENSE_LABEL`) to an **array of complete pt-PT sentences**. Nothing is assembled at runtime — the sentences are written whole by the LLM (see `prompt.md`).
- Each sentence contains **exactly one inline marker** `{…}` wrapping the conjugated form to be blanked, e.g. `"Ontem eu {comi} uma maçã."`. Clitics and hyphens go inside the marker (`{levanto-me}`, `{levanta-te}`); an imperative sentence starts with the marker (`"{Come} a sopa, por favor!"`). A sentence must contain no other `{` or `}`.
- `buildQuestion(verb, tk, idx)` takes `verb.phrases[tk][idx]` and `parsePhrase` splits it at the first marker → `{ sentence (marker replaced by the `@@VERB@@` sentinel), answer (marker content) }`. A phrase with no marker, an empty marker, or a missing/empty tense array returns null and is skipped.
- Each tense holds 5 sentences covering eu / tu / ele-ela-você / nós / eles-elas-vocês (the subject must be visible in the sentence). `imperativo_afirmativo` holds 4 and omits `eu`. Missing tense keys are skipped.
- Tense keys are read dynamically via `Object.keys`, so a new tense needs no logic change. Add it to the data and to `TENSE_META`/`TENSE_LABEL` for display. Unknown keys fall back to the `Outros` mood group.
- Capitalisation and punctuation come from the data as written; the runtime only collapses repeated spaces and drops spaces before `.,!?;:`.

## Conventions
- Answer matching uses `String(s).normalize("NFC").replace(/[\s-]+/g, "").toLowerCase()` — it normalizes Unicode (so decomposed accents compare equal), then strips **all** whitespace and hyphens, so `"co mem"` matches `"comem"` and `"lembrome"` matches `"lembro-me"`.
- Fonts load via a Google Fonts `@import` at the top of the inline `<style>` (`Huninn`, `Noto Sans HK`), wired through `--font-display`/`--font-body` with system fallbacks; `--font-mono` stays a system stack. This is the sole network request.
- Keep it client-only and dependency-free; the only storage exceptions are `localStorage.theme` (theme toggle), `localStorage["ptvg.checked"]` (selected tenses, JSON array), and `localStorage["ptvg.stats"]` (`{correct,total}`, JSON). The theme is set by an inline `<head>` script to avoid flash, with OKLCH variables overridden under `:root[data-theme="dark"]`.

## Tooling internals (gitignored, do not touch)
- `.od-skills/`, `.file-versions/` (Open Design folders). `verb-game.html.artifact.json` is Open Design renderer metadata.
