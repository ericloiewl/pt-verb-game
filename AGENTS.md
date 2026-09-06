# AGENTS.md

Two-file, self-contained web project (no build, no install, no tests).

## What this is
- `verb-game.html` contains markup, inline `<style>`, and inline game logic. `verb-data.js` contains only game data (`window.VERB_DATA`) and is loaded via `<script src>`.
- No bundler, framework, package.json, or dependency. Open `verb-game.html` directly in a browser. It makes no external/network requests.

## Data model (do not violate)
- All game content lives in `verb-data.js` as `window.VERB_DATA`, an array of verb objects.
- Each verb: `infinitive` + `tenses`, where each tense has:
  - `conjugations`: object keyed by person string (`"eu"`, `"tu"`, `"ele/ela/você"`, `"nós"`, `"eles/elas/vocês"`) — keys must match `PERSON` in the HTML.
  - `suffixes`: shared pool of sentence endings. A question sentence is assembled at runtime as `subject + " ___ " + suffix` (random suffix, random subject from `PERSON_DISPLAY`, where `ele/ela/você` and `eles/elas/vocês` randomly display as Ele/Ela/Você and Eles/Elas/Vocês).
- Tense keys (e.g. `presente`, `preterito_perfeito`) are read dynamically via `Object.keys`, so adding a tense needs no code change.
- The two example verb objects (`comer`, `falar`) must be kept verbatim. Only **append** new verb objects to extend the dataset.

## Conventions
- Answer matching uses `trim().toLowerCase()`, so `"  COMEM "`, `"comem"`, and `"ComEm"` are all correct.
- Keep it client-only and dependency-free; do not introduce servers, storage, audio, or timers unless asked.
- `verb-game-plan.md` is the source-of-truth spec. Edit it if behavior changes.

## Tooling internals (gitignored, do not touch)
- `.od-skills/` and `.file-versions/` are Open Design environment folders, not project source.
