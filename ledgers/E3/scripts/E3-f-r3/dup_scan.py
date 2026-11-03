"""Duplicate scan for the E3 L01-L04 retrieval cards (verifier E3 slice f, round 3).

For every pair of slice cards (lesson L01-L04) it prints the front and back similarity (difflib ratio on lowercased
words) and the count of shared content words, sorted by the larger of the two scores. Run with -I.
"""

from __future__ import annotations

import difflib
import json
import re
import sys

PATH = sys.argv[1]
cards = [c for c in json.load(open(PATH, encoding="utf-8")) if c["lesson"] in ("L01", "L02", "L03", "L04")]
STOP = {"the", "a", "an", "of", "and", "is", "to", "for", "in", "on", "with", "that", "it", "its", "by", "as", "at",
        "under", "does", "do", "not", "no", "yes", "which", "what", "how", "when", "this", "be", "or", "if", "then",
        "so", "are", "was", "from", "each", "every", "one", "all", "only", "than", "has", "have", "into", "over"}


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9_]+", s.lower()) if w not in STOP and len(w) > 1}


rows = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        fr = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        bk = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        shared = words(a["back"]) & words(b["back"])
        rows.append((max(fr, bk), fr, bk, len(shared), a["id"], a["lesson"], b["id"], b["lesson"]))
print(f"slice cards: {len(cards)}; pairs: {len(rows)}")
print("top 25 pairs by max(front ratio, back ratio): max fr bk shared_back_words | id(lesson) id(lesson)")
for mx, fr, bk, sh, ia, la, ib, lb in sorted(rows, reverse=True)[:25]:
    print(f"{mx:.3f} {fr:.3f} {bk:.3f} {sh:3d} | {ia}({la}) {ib}({lb})")
ids = [c["id"] for c in cards]
print("duplicate ids:", sorted({x for x in ids if ids.count(x) > 1}))
