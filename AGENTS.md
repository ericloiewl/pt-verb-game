# AGENTS.md

Self-contained static web game: no build, install, tests, or dependencies. Open `index.html` directly in a browser; it makes no network requests.

## Files
- `index.html` — markup, inline `<style>`, and inline game logic. Runtime behavior lives here and it is the GitHub Pages entry point.
- `verb-data.js` — `window.VERB_DATA` dataset, loaded via `<script src>`. Sole copy of the dataset.
- `prompt.md` — LLM prompt that was used to generate the dataset (provenance only, not loaded at runtime).
- `README.md` — project overview.

## Data editing (gotcha)
- The dataset lives only in `verb-data.js` (`window.VERB_DATA = {...};`); edit it directly and keep it valid JS.
- Keep the file self-contained: no network requests, no dependencies.

## Data model (do not violate)
- Each verb: `infinitive`, `translation_zh`/`translation_en`, `type`, `group`, `reflexive`, `objects` pool, `sentence_template`, `notes`, `tenses`.
- Each tense: `name`, `type` (`indicative`/`subjunctive`/`imperative`), `conjugations` (keyed by person), `time_markers`, `special_templates`.
- Question assembly (`buildQuestion`): if `special_templates` is non-empty use it, else fall back to the verb-level `sentence_template`. Placeholders: `{time_marker}` (tense pool), `{subject}` (`PERSON_DISPLAY`), `{object}` (`verb.objects`), `{reflexive_pronoun}` (forward-compat), and `{verb}` → the blank. The answer is the full `conjugations[person]` (reflexive clitics included).
- Person keys must match `PERSON` in the HTML: `eu`, `tu`, `ele/ela/você`, `nós`, `eles/elas/vocês`. `imperativo_afirmativo` intentionally omits `eu`; `buildQuestion` returns null for missing keys and skips them.
- Tense keys are read dynamically via `Object.keys`, so a new tense needs no logic change. Add it to the data and to `TENSE_META`/`TENSE_LABEL` for display. Unknown keys fall back to the `Outros` mood group.
- Subjects are substituted lowercase (they sit mid-sentence); the final sentence's first letter is capitalized.

## Conventions
- Answer matching uses `String(s).normalize("NFC").replace(/[\s-]+/g, "").toLowerCase()` — it normalizes Unicode (so decomposed accents compare equal), then strips **all** whitespace and hyphens, so `"co mem"` matches `"comem"` and `"lembrome"` matches `"lembro-me"`.
- Keep it client-only and dependency-free; the only storage exceptions are `localStorage.theme` (theme toggle), `localStorage["ptvg.checked"]` (selected tenses, JSON array), and `localStorage["ptvg.stats"]` (`{correct,total}`, JSON). The theme is set by an inline `<head>` script to avoid flash, with OKLCH variables overridden under `:root[data-theme="dark"]`.

## Tooling internals (gitignored, do not touch)
- `.od-skills/`, `.file-versions/` (Open Design folders). `verb-game.html.artifact.json` is Open Design renderer metadata.
