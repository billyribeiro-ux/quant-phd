"""Verifier M7 slice a round 1: per-card byte comparison of cards.json between the base pin and HEAD.

Usage: card_bytes_delta.py <base-commit> <head-commit>. Reads the two versions with git show, groups each card
object by its id, and prints which cards are byte-identical (after re-serialisation with a fixed key order) and
which differ, separately for L01-L03 and for the rest of the file.
"""
import json
import subprocess
import sys
from collections import Counter

base, head = sys.argv[1], sys.argv[2]
path = "course/modules/M/M7/cards.json"


def load(rev: str) -> list[dict]:
    raw = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


def ser(c: dict) -> str:
    return json.dumps(c, ensure_ascii=False, sort_keys=True)


b = {c["id"]: c for c in load(base)}
h = {c["id"]: c for c in load(head)}
print("base cards", len(b), "head cards", len(h))
print("added in head:", sorted(set(h) - set(b)))
print("removed in head:", sorted(set(b) - set(h)))
changed = sorted(k for k in set(b) & set(h) if ser(b[k]) != ser(h[k]))
print("changed (all lessons):", changed)
for L in ("L01", "L02", "L03"):
    ids = sorted(k for k, v in h.items() if v["lesson"] == L)
    same = [k for k in ids if k in b and ser(b[k]) == ser(h[k])]
    diff = [k for k in ids if k not in same]
    print(f"{L}: head {len(ids)} cards, byte-identical to base {len(same)}, changed or new {diff}")
