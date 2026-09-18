# AGENTS.md

Self-contained static web game: no build, install, tests, or dependencies. Open `verb-game.html` directly in a browser; it makes no network requests.

## Files
- `verb-game.html` — markup, inline `<style>`, and inline game logic. Runtime behavior lives here.
- `verb-data.js` — `window.VERB_DATA` dataset, loaded via `<script src>`. Generated; do not hand-edit.
- `new-verb-data.json` — source of truth for the dataset (LLM-generated per `prompt.md`): 5 verbs x 8 tenses, rich lexical fields + sentence templates.
- `gen.py` — legacy Python 3 generator for the old schema (50 verbs, `suffixes` pools). No longer produces `verb-data.js`.
- `verb-game-plan.md` / `README.md` — design spec, partly stale. Trust `verb-game.html`/`new-verb-data.json` over the prose when they conflict.

## Data regeneration (gotcha)
- `verb-data.js` is exactly `window.VERB_DATA = <new-verb-data.json>;`. Regenerate after editing the JSON (UTF-8):
  `python -c "import json;d=json.load(open('new-verb-data.json',encoding='utf-8'));open('verb-data.js','w',encoding='utf-8').write('window.VERB_DATA = '+json.dumps(d,ensure_ascii=False,indent=2)+';')"`
- Never edit the generated ~900-line `verb-data.js` by hand.
- `gen.py` still writes `verbos.json` (old schema) and its final `print` raises `UnicodeEncodeError` on a cp950 Windows console; it just isn't part of the current pipeline.

## Data model (do not violate)
- Each verb: `infinitive`, `translation_zh`/`translation_en`, `type`, `group`, `reflexive`, `objects` pool, `sentence_template`, `notes`, `tenses`.
- Each tense: `name`, `type` (`indicative`/`subjunctive`/`imperative`), `conjugations` (keyed by person), `time_markers`, `special_templates`.
- Question assembly (`buildQuestion`): if `special_templates` is non-empty use it, else fall back to the verb-level `sentence_template`. Placeholders: `{time_marker}` (tense pool), `{subject}` (`PERSON_DISPLAY`), `{object}` (`verb.objects`), `{reflexive_pronoun}` (forward-compat), and `{verb}` → the blank. The answer is the full `conjugations[person]` (reflexive clitics included).
- Person keys must match `PERSON` in the HTML: `eu`, `tu`, `ele/ela/você`, `nós`, `eles/elas/vocês`. `imperativo_afirmativo` intentionally omits `eu`; `buildQuestion` returns null for missing keys and skips them.
- Tense keys are read dynamically via `Object.keys`, so a new tense needs no logic change. Add it to the data and to `TENSE_META`/`TENSE_LABEL` for display. Unknown keys fall back to the `Outros` mood group.
- Subjects are substituted lowercase (they sit mid-sentence); the final sentence's first letter is capitalized.

## Conventions
- Answer matching uses `String(s).replace(/[\s-]+/g, "").toLowerCase()` — it strips **all** whitespace and hyphens, so `"co mem"` matches `"comem"` and `"lembrome"` matches `"lembro-me"`.
- Keep it client-only and dependency-free; the only storage exception is `localStorage.theme` (theme toggle). The theme is set by an inline `<head>` script to avoid flash, with OKLCH variables overridden under `:root[data-theme="dark"]`.

## Tooling internals (gitignored, do not touch)
- `.od-skills/`, `.file-versions/` (Open Design folders). `verb-game.html.artifact.json` is Open Design renderer metadata.
