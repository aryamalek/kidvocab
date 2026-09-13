# Vocabulary plan

Shared planning memory for Little Words. Any session (either parent, any device)
that discusses what to teach next should read this first and record decisions
here — otherwise plans made in one chat are invisible to the next.

These are working notes, not rules — either parent can override, reorder, or
rewrite any of it at any time. Changing your mind is part of the process; when
that happens, update this file to the new thinking.

## Principles for picking words (he's 2.5)

- Concrete things he can see, touch, or point at — nouns first.
- His actual daily world beats "classic flashcard" words: his food, his toys,
  his routines.
- High-frequency across all three households' languages; skip words the
  parents rarely say.
- Batch by theme (5–8 words) — themes make good demo/play sessions.

## Covered so far

- Animals, food & drink, body, vehicles, home & play, nature — 45 words
  (initial set, 2026-09-13).
- Shapes — 22 words: the full 2D set (incl. crescent, cross, arrow, star) plus
  3D solids (sphere, cube, cone, cylinder, pyramid) (2026-09-13, Arya's request).
- Emotions — 16 words, aimed at 2–6 (2026-09-13, Maria's request): the six he
  can use now (happy, sad, angry, tired, scared, cry), then laugh, love,
  surprised, shy, excited, and the older ones — proud, calm, jealous, lonely,
  brave. Words only so far: pictures and recorded voices still to come.

## Backlog — next themes to consider

- Playground (Rutsche, Schaukel, Sandkasten…) — queued as Maria's first demo
- Clothes (jacket, hat, socks…)
- Bath time (bathtub, soap, towel…)
- Weather beyond rain/sun (snow, wind, cloud)
- Family words (Mama, Papa, grandma/grandpa in all three languages)
- First adjectives when ready: big/small, hot/cold, colors

## Decisions log

- 2026-09-13: shapes theme added at Arya's request, including advanced shapes
  (parallelogram, rhombus, trapezoid…) — going past age-typical vocabulary on
  purpose. Six shapes ARASAAC lacks (trapezoid, octagon, semicircle, crescent,
  cross, arrow) are hand-drawn in images/ in the same outline style; don't
  delete those files, fetch_images.py can't re-create them.
- 2026-09-13: cards grouped into decks (cat field + header chip); star moved
  from nature to shapes. Default deck set to Shapes while that's the focus.
- 2026-09-13: emotions added as the next theme at Maria's request; Emotions is
  now the first deck, so it's what the app opens with. Emotion words are
  adjectives — no German article, unlike every other deck.
  Still open: that session could not reach ARASAAC or the voice service
  (blocked by its network policy), so the 16 emotion cards have no pictogram
  and no recorded voices yet. Next session with reach: run fetch_images.py,
  look at each new images/<word>.png (emotion faces are easy to get wrong —
  "cry" and "sad" often come back as the same picture), then fetch_audio.py,
  then validate.py. Arya: please check the Persian vowelization on those 16.

- 2026-09-13: start with 45-word core set; images = ARASAAC, audio = two
  alternating voices per language, first voice matches the parent.
