# Little Words — kidvocab

Trilingual (English / German / Farsi) picture-flashcard web app for a 2.5-year-old.
Single self-contained page, deployed via GitHub Pages: https://aryamalek.github.io/kidvocab/
Pushing to `main` redeploys automatically (~1 min). Requests may arrive in German —
Maria (the child's mother, German speaker) is a primary user of this repo.

## Adding or changing words — the full workflow

1. Edit the `VOCAB` list at the top of `index.html`. One line per word:
   `{ emoji: "🐸", en: "frog", de: "der Frosch", fa: "قورباغه", faLatin: "ghurbāgheh" },`
   - German always includes the article (der/die/das) — gender matters for learning.
   - `faLatin` is a simple readable transliteration (ā for long a, kh/gh/sh digraphs,
     -eh endings: gorbeh, setāreh). Match the existing entries' style.
   - The emoji is only a fallback shown until an image is fetched.
2. Run `python3 fetch_images.py` — finds an ARASAAC pictogram per new word,
   caches it in `images/`, embeds it into `index.html` as a data URI.
3. **Look at every newly fetched `images/<word>.png`** (read the image file) and
   confirm it clearly depicts the word for a 2-year-old. Keyword search picks
   wrong concepts regularly — if it's off, pick a better pictogram (see below).
4. Run `python3 fetch_audio.py` (needs `pip install edge-tts`) — generates spoken
   clips for all three languages, two voices each (taps alternate voices; the first
   voice matches the parent who speaks that language: Farsi male, German female).
5. Run `python3 validate.py` — must print `ok` before you push. The same check
   runs as a GitHub Action on every push.
6. Commit everything (including `images/`, `audio/`, and the regenerated
   `index.html`) and push **directly to `main`** — do not open a PR unless the
   change is risky. Pages redeploys in ~1 min and the app on each device
   refreshes itself next time it's opened.

## Talking to the family

Requests often come from a parent on a phone, mid-life, possibly in German —
answer in the language you were addressed in. Narrate what you're doing in
plain, non-technical language as you go (finding pictures, checking them,
recording the voices, publishing), not in git/CI vocabulary. When you finish,
say clearly: the words are live at https://aryamalek.github.io/kidvocab/ —
close and reopen the app and they'll be there.

Both scripts are idempotent: they skip words that already have cached files, so
re-running is always safe.

## If an auto-picked image is wrong

Search https://arasaac.org for the word, add `arasaac: <id>,` to that word's line
in VOCAB, delete `images/<word>.png`, re-run `fetch_images.py`. Past mistakes were
concept mismatches (a cooked fish for "fish", a high heel for "shoe") — always
prefer the toddler-obvious depiction of a word.

## Rules that keep the app what it is

- One file, no framework, no build step. Do not add dependencies or split it up.
- `index.html` structure: human-edited VOCAB at the top; the AUDIO and IMAGES
  blocks near the bottom are machine-generated — never edit them by hand.
- No emoji as card art (fallback only), no flags, all four word rows equal size.
- Everything must be embedded (data URIs) — the page must work offline once loaded.
- Keep it toddler-proof and instant: no menus, no settings screens, no accounts.
