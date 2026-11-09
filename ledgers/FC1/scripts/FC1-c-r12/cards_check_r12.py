"""Full scan of FC1 cards.json (slice c, round 12): schema, unique ids, unique fronts, lesson existence, numbers in
back that also appear in the card's lesson text, and the round-12 changed cards (c152, c153)."""
from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-FC1-c/course/modules/FC/FC1")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
keys = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", {tuple(k): v for k, v in keys.items()})
print("grades:", Counter(c.get("grade") for c in cards))
lessons = {}
for n in ("L01", "L02", "L03", "L04", "L05"):
    raw = (ROOT / f"{n}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    lessons[n] = html.unescape(re.sub(r"\s+", " ", raw))
bad_lesson = [c["id"] for c in cards if c["lesson"] not in lessons]
print("cards with unknown lesson:", bad_lesson)
num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
missing = []
for c in cards:
    nums = set(num_re.findall(c["back"])) | set(num_re.findall(c["front"]))
    text = lessons.get(c["lesson"], "")
    for n in nums:
        bare = n.replace(",", "")
        if bare in ("1", "0", "2", "3") or len(bare) <= 1:
            continue
        if n not in text and bare not in text:
            missing.append((c["id"], n))
print("numbers (>=2 digits) in card not found in its lesson text:", len(missing))
for m in missing[:60]:
    print("   ", m)
for cid in ("FC1-c147", "FC1-c150", "FC1-c152", "FC1-c153", "FC1-c014", "FC1-c122", "FC1-c030", "FC1-c139", "FC1-c142", "FC1-c143", "FC1-c151"):
    for c in cards:
        if c["id"] == cid:
            print(json.dumps(c, ensure_ascii=False))
