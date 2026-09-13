#!/usr/bin/env python3
"""Sanity-check index.html before deploying.

Usage: python3 validate.py   (exit code 0 = safe to push)

Catches the ways a conversational edit can silently break the app: a word
missing its image or audio clips, Farsi that isn't in Persian script,
duplicate words, or a German entry without its article.
"""

import re
import sys
from pathlib import Path

html = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

ENTRY_RE = re.compile(
    r'\{\s*emoji:\s*"([^"]*)"\s*,\s*en:\s*"([^"]+)"\s*,'
    r'(?:\s*arasaac:\s*\d+\s*,)?\s*de:\s*"([^"]+)"\s*,'
    r'\s*fa:\s*"([^"]+)"\s*,\s*faLatin:\s*"([^"]+)"')


def block(name):
    start = html.index(f"const {name} = ")
    return html[start:html.index("\n};", start)] + "\n"


errors, warnings = [], []

vocab = ENTRY_RE.findall(block("VOCAB"))
if not vocab:
    sys.exit("FAIL: no VOCAB entries parsed from index.html")

words = [en for _, en, _, _, _ in vocab]
for w in sorted({w for w in words if words.count(w) > 1}):
    errors.append(f'duplicate word "{w}" in VOCAB')

cats_by_word = dict(re.findall(r'en:\s*"([^"]+)".*?cat:\s*"([^"]+)"', block("VOCAB")))

for emoji, en, de, fa, fa_latin in vocab:
    if not emoji:
        warnings.append(f"{en}: empty emoji fallback")
    if not re.search(r"[؀-ۿ]", fa):
        errors.append(f"{en}: fa \"{fa}\" is not in Persian script")
    if re.search(r"[؀-ۿ]", fa_latin):
        errors.append(f"{en}: faLatin \"{fa_latin}\" contains Persian script")
    # emotion words are adjectives (traurig, müde) — no article to carry
    if cats_by_word.get(en) != "emotions" and not re.match(r"(der|die|das)\s", de):
        warnings.append(f'{en}: de "{de}" has no article (der/die/das)')

KNOWN_CATS = {"animals", "food", "body", "vehicles", "home", "nature", "shapes",
              "emotions"}
cats = re.findall(r'cat: "([^"]+)"', block("VOCAB"))
if len(cats) != len(vocab):
    errors.append(f"{len(vocab) - len(cats)} VOCAB entries missing a cat field")
for c in set(cats) - KNOWN_CATS:
    errors.append(f'unknown cat "{c}" (add it to KNOWN_CATS here and DECKS in the app)')

images = set(re.findall(r'"([^"]+)": "data:image/png', block("IMAGES")))
for en in words:
    if en not in images:
        errors.append(f"{en}: no embedded image (run fetch_images.py)")
for extra in images - set(words):
    warnings.append(f'IMAGES has orphan entry "{extra}" (word no longer in VOCAB)')

audio_block = block("AUDIO")
audio_entries = dict(re.findall(r'"([^"]+)": (\{.*?\}),?\n', audio_block))
for en in words:
    entry = audio_entries.get(en)
    if entry is None:
        errors.append(f"{en}: no audio at all (run fetch_audio.py)")
        continue
    for lang in ("en", "de", "fa"):
        clips = re.search(rf"{lang}: \[([^\]]*)\]", entry)
        n = clips.group(1).count("data:audio") if clips else 0
        if n < 2:
            errors.append(f"{en}: {lang} audio has {n}/2 clips (run fetch_audio.py)")
for extra in set(audio_entries) - set(words):
    warnings.append(f'AUDIO has orphan entry "{extra}" (word no longer in VOCAB)')

if not html.rstrip().endswith("</html>"):
    errors.append("index.html does not end with </html> — file may be truncated")

for w in warnings:
    print(f"warn: {w}")
if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)
print(f"ok: {len(vocab)} words, all with images and 6 audio clips")
