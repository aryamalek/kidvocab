#!/usr/bin/env python3
"""Fill in spoken audio for every word in index.html's VOCAB list.

Usage: python3 fetch_audio.py   (needs: pip install edge-tts)

For each vocab entry, generates a short TTS clip (Microsoft neural voices,
via edge-tts) for English, German, and Farsi, caches the mp3s in audio/,
then regenerates the AUDIO block in index.html as base64 data URIs. The app
plays the clip when a word is tapped; words without a clip fall back to the
device's own voice. Delete a file in audio/ to re-fetch it.
"""

import asyncio
import base64
import re
import sys
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
HTML = HERE / "index.html"
AUDIO_DIR = HERE / "audio"
# first voice = the parent who speaks that language (fa: dad, de: mom);
# taps alternate through the list
VOICES = {
    "en": ["en-US-JennyNeural", "en-US-GuyNeural"],
    "de": ["de-DE-KatjaNeural", "de-DE-ConradNeural"],
    "fa": ["fa-IR-FaridNeural", "fa-IR-DilaraNeural"],
}
RATE = "-20%"  # slower, for a toddler

ENTRY_RE = re.compile(
    r'\{\s*emoji:.*?en:\s*"([^"]+)".*?de:\s*"([^"]+)".*?fa:\s*"([^"]+)"', re.S)


async def fetch(text, voice, path):
    await edge_tts.Communicate(text, voice, rate=RATE).save(str(path))


def main():
    html = HTML.read_text(encoding="utf-8")
    AUDIO_DIR.mkdir(exist_ok=True)

    vocab_block = html[html.index("const VOCAB"):html.index("];", html.index("const VOCAB"))]
    entries = ENTRY_RE.findall(vocab_block)
    if not entries:
        sys.exit("No VOCAB entries found in index.html")

    audio, failed = {}, []
    for en, de, fa in entries:
        clips = {}
        for lang, text in (("en", en), ("de", de), ("fa", fa)):
            uris = []
            for i, voice in enumerate(VOICES[lang]):
                path = AUDIO_DIR / f"{en.replace(' ', '_')}_{lang}_{i}.mp3"
                if not path.exists():
                    try:
                        asyncio.run(fetch(text, voice, path))
                        print(f"fetched {en} [{lang} {voice}]")
                    except Exception as e:
                        path.unlink(missing_ok=True)
                        failed.append(f"{en} [{lang} {voice}]: {e}")
                        continue
                uris.append("data:audio/mpeg;base64,"
                            + base64.b64encode(path.read_bytes()).decode())
            if uris:
                clips[lang] = uris
        if clips:
            audio[en] = clips

    block = "const AUDIO = {\n" + "".join(
        f'  "{w}": {{'
        + ", ".join(f'{l}: [' + ", ".join(f'"{u}"' for u in uris) + "]"
                    for l, uris in clips.items())
        + "},\n" for w, clips in audio.items()) + "};"
    html, n = re.subn(r"const AUDIO = \{.*?\};", block, html, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the AUDIO block in index.html")
    HTML.write_text(html, encoding="utf-8")

    total = sum(len(u) for c in audio.values() for v in c.values() for u in v)
    print(f"\n{len(audio)}/{len(entries)} words have audio ({total / 1e6:.1f} MB embedded)")
    if failed:
        print("failed (device voice will be used):")
        for f in failed:
            print("  " + f)


if __name__ == "__main__":
    main()
