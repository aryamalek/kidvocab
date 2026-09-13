#!/usr/bin/env python3
"""Fill in ARASAAC pictograms for every word in index.html's VOCAB list.

Usage: python3 fetch_images.py

For each vocab entry, searches ARASAAC by the English word, downloads the
pictogram once into images/, then regenerates the IMAGES block in index.html
as base64 data URIs. Entries can pin a specific pictogram with an
`arasaac: <id>` field (find ids at https://arasaac.org by searching the word).
Words with no match are reported and keep their emoji fallback.
"""

import base64
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "index.html"
IMG_DIR = HERE / "images"
API = "https://api.arasaac.org/api/pictograms"
STATIC = "https://static.arasaac.org/pictograms/{id}/{id}_500.png"

ENTRY_RE = re.compile(r'\{\s*emoji:.*?en:\s*"([^"]+)".*?\}', re.S)
ARASAAC_RE = re.compile(r'arasaac:\s*(\d+)')


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "littlewords/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def find_pictogram_id(word):
    for endpoint in ("bestsearch", "search"):
        try:
            results = json.loads(get(f"{API}/en/{endpoint}/{urllib.parse.quote(word)}"))
            if results:
                return results[0]["_id"]
        except Exception:
            continue
    return None


def main():
    html = HTML.read_text(encoding="utf-8")
    IMG_DIR.mkdir(exist_ok=True)

    vocab_block = html[html.index("const VOCAB"):html.index("];", html.index("const VOCAB"))]
    entries = []
    for m in ENTRY_RE.finditer(vocab_block):
        pinned = ARASAAC_RE.search(m.group(0))
        entries.append((m.group(1), int(pinned.group(1)) if pinned else None))
    if not entries:
        sys.exit("No VOCAB entries found in index.html")

    images, missing = {}, []
    for word, pinned in entries:
        path = IMG_DIR / f"{word.replace(' ', '_')}.png"
        if not path.exists():
            pid = pinned or find_pictogram_id(word)
            if pid is None:
                missing.append(word)
                continue
            path.write_bytes(get(STATIC.format(id=pid)))
            print(f"fetched {word} (pictogram {pid})")
        images[word] = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()

    block = "const IMAGES = {\n" + "".join(
        f'  "{w}": "{uri}",\n' for w, uri in images.items()) + "};"
    html, n = re.subn(r"const IMAGES = \{.*?\};", block, html, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the IMAGES block in index.html")
    HTML.write_text(html, encoding="utf-8")

    print(f"\n{len(images)}/{len(entries)} words have images "
          f"({sum(len(v) for v in images.values()) / 1e6:.1f} MB embedded)")
    if missing:
        print("no pictogram found for: " + ", ".join(missing))
        print("→ pin one manually: add `arasaac: <id>` to the entry in index.html")
    if len(images) < len(entries) - len(missing):
        print("note: some cached images/ files may be stale — delete a file to re-fetch")


if __name__ == "__main__":
    main()
