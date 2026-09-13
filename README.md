# Little Words

Trilingual (EN / DE / FA) picture flashcards for a toddler.
Published at: https://claude.ai/code/artifact/b2f2e014-4a58-48cf-ae42-56a3deabbb48

## Adding words

1. Add a line to the `VOCAB` list at the top of `index.html`:
   `{ emoji: "🐸", en: "frog", de: "der Frosch", fa: "قورباغه", faLatin: "ghurbāgheh" },`
   (the emoji is only the fallback shown until an image is fetched)
2. Run `python3 fetch_images.py` — it finds an ARASAAC pictogram for each new
   word and embeds it into `index.html`.
   Then `python3 fetch_audio.py` — it generates spoken clips (Microsoft neural
   voices via edge-tts) for all three languages; tapping a word plays its clip.
3. If the auto-picked image is wrong, find a better one at https://arasaac.org,
   add `arasaac: <id>,` to that word's line, delete `images/<word>.png`, re-run.
4. Ask Claude to republish (or do all of the above by just telling Claude the
   new words — it redeploys to the same URL).

Images are ARASAAC pictograms (CC BY-NC-SA, free for personal use), cached in
`images/` and embedded into the single-file app as data URIs.
