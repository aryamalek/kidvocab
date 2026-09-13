# Little Words

Trilingual (EN / DE / FA) picture flashcards for a toddler.
Live at: https://aryamalek.github.io/kidvocab/ (GitHub Pages, repo aryamalek/kidvocab)

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
4. Commit and `git push` — GitHub Pages redeploys in about a minute.
   (Or just tell Claude the new words — it does all of the above.)

Images are ARASAAC pictograms (CC BY-NC-SA, free for personal use), cached in
`images/` and embedded into the single-file app as data URIs.
