# AGENTS.md

Single-file, self-contained web project (no build, no install, no tests).

## What this is
- `verb-game.html` contains everything: markup, inline `<style>`, and inline JS. There is no bundler, framework, package.json, or dependency.
- Open it directly in a browser. It makes no external/network requests.

## Data model (do not violate)
- All game content lives in the inline `verbData` array.
- Each verb: `infinitive` + `tenses`, where each tense has `conjugations` and `sentences`, both length-5 arrays.
- Index order is the grammatical person: 0=eu, 1=tu, 2=ele/ela/você, 3=nós, 4=eles/elas/vocês. Keep these aligned with the `___` placeholder in each sentence.
- Tense keys (e.g. `presente`, `preterito_perfeito`) are read dynamically via `Object.keys`, so adding a tense needs no code change.
- The two example verb objects (`comer`, `falar`) must be kept verbatim. Only **append** new verb objects to extend the dataset.

## Conventions
- Answer matching uses `trim().toLowerCase()`, so `"  COMEM "`, `"comem"`, and `"ComEm"` are all correct.
- Keep it client-only and dependency-free; do not introduce servers, storage, audio, or timers unless asked.
- `verb-game-plan.md` is the source-of-truth spec. Edit it if behavior changes.

## Tooling internals (gitignored, do not touch)
- `.od-skills/` and `.file-versions/` are Open Design environment folders, not project source.
