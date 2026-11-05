"""M2-d2 r10: card census, duplicate scan and slice delta against the round-9 pin.

Usage (from checkout root): .venv/bin/python ledgers/M2/scripts/M2-d2-r10/cards_delta.py
Reads the working tree cards.json and the round-9 pin's cards.json via git show.
"""
import collections
import json
import subprocess
import sys

CUR = "course/modules/M/M2/cards.json"
PREV_PIN = "1e272e5a641f18412703b37778a44db6f7391a69"
SLICE = {"L22", "L23", "L24"}

cur = json.load(open(CUR, encoding="utf-8"))
prev_raw = subprocess.run(["git", "show", f"{PREV_PIN}:{CUR}"], capture_output=True, text=True, check=True).stdout
prev = json.loads(prev_raw)

print("cards total now:", len(cur), " at r9 pin:", len(prev))
ids = [c["id"] for c in cur]
dup_ids = [k for k, v in collections.Counter(ids).items() if v > 1]
print("duplicate ids:", dup_ids)
fronts = collections.Counter(" ".join(c["front"].split()).lower() for c in cur)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(" ".join(c["back"].split()).lower() for c in cur)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
per = collections.Counter(c["lesson"] for c in cur if c["id"].startswith("M2-"))
print("per-lesson counts M2:", dict(sorted(per.items())))
for L in sorted(SLICE):
    sel = [c["id"] for c in cur if c["lesson"] == L]
    print(L, len(sel), sel)
prev_by_id = {c["id"]: c for c in prev}
cur_by_id = {c["id"]: c for c in cur}
changed = [i for i in cur_by_id if i in prev_by_id and cur_by_id[i] != prev_by_id[i]]
added = [i for i in cur_by_id if i not in prev_by_id]
removed = [i for i in prev_by_id if i not in cur_by_id]
print("changed vs r9 pin:", changed)
print("added vs r9 pin:", added)
print("removed vs r9 pin:", removed)
for i in changed + added:
    c = cur_by_id[i]
    print(i, c["lesson"], "slice" if c["lesson"] in SLICE else "outside-slice")
print("slice cards changed vs r9 pin:", [i for i in changed if cur_by_id[i]["lesson"] in SLICE])
print("slice cards added vs r9 pin:", [i for i in added if cur_by_id[i]["lesson"] in SLICE])
sys.exit(0)
