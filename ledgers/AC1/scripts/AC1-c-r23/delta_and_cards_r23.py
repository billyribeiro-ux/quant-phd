"""Round 23 (AC1-c): byte-identity of slice files since the previous pin, and card checks.

Usage: python -I delta_and_cards_r23.py <checkout> <previous_pin>
Prints the sha256 of each slice file at the previous pin and at HEAD, then compares the
L07 and L08 card objects (lesson L07 or L08) and scans cards.json for duplicate ids and fronts.
"""

import hashlib
import json
import subprocess
import sys
from collections import Counter

root, pin = sys.argv[1], sys.argv[2]
files = [
    "course/modules/AC/AC1/L07.html",
    "course/modules/AC/AC1/L08.html",
    "course/modules/AC/AC1/index.html",
    "course/modules/AC/AC1/project.html",
    "tests/labs/AC1/lab-AC1-L07-1.py",
    "tests/labs/AC1/lab-AC1-L08-1.py",
    "references/references.json",
]


def blob(rev: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, check=True).stdout


all_same = True
for f in files:
    a, b = blob(pin, f), blob("HEAD", f)
    same = a == b
    all_same &= same
    print(f"{f}: {'byte-identical' if same else 'CHANGED'} sha256={hashlib.sha256(b).hexdigest()[:16]}")
print("all slice files byte-identical:", all_same)

cards_now = json.loads(blob("HEAD", "course/modules/AC/AC1/cards.json"))
cards_pin = json.loads(blob(pin, "course/modules/AC/AC1/cards.json"))
sl_now = [c for c in cards_now if c["lesson"] in ("L07", "L08")]
sl_pin = [c for c in cards_pin if c["lesson"] in ("L07", "L08")]
print("L07/L08 cards at pin:", len(sl_pin), "at HEAD:", len(sl_now), "identical:", sl_now == sl_pin)
print("cards total at pin:", len(cards_pin), "at HEAD:", len(cards_now))
ids = Counter(c["id"] for c in cards_now)
fronts = Counter(c["front"].strip().lower() for c in cards_now)
backs = Counter(c["back"].strip().lower() for c in cards_now)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
changed_ids = [c["id"] for c in cards_now if c not in cards_pin]
print("cards at HEAD not byte-identical in content to the pin (ids):", changed_ids)
