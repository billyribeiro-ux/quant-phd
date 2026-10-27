"""Round 28: W4 (\\d for [0-9]) and W6 (search for fullmatch) on Python 3.14.
W4: every date string whose ASCII digits are replaced by other Unicode decimal digits, which the \\d regex admits, is refused by date.fromisoformat.
W6: fromisoformat accepts only strings of length <= 10, so no accepted string can properly contain a 10-character YYYY-MM-DD match.
Usage: python -I equiv_w4_w6_r28B_b.py"""
import random
import re
import unicodedata
from datetime import date

rng = random.Random(20261104)
digits_by_script = {}
for cp in range(0x110000):
    try:
        ch = chr(cp)
    except ValueError:
        continue
    if unicodedata.category(ch) == "Nd":
        digits_by_script.setdefault(unicodedata.name(ch).split(" DIGIT")[0], []).append(ch)
scripts = [v for v in digits_by_script.values() if len(v) >= 10]
print("Unicode decimal digit scripts (>=10 digits):", len(scripts))
ISO_D = re.compile(r"\d{4}-\d{2}-\d{2}")
ISO_A = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
bad = admitted = 0
for _ in range(20000):
    y, m, d = rng.randint(1990, 2030), rng.randint(1, 12), rng.randint(1, 28)
    s = f"{y:04d}-{m:02d}-{d:02d}"
    sc = rng.choice(scripts)
    t = "".join(sc[ord(c) - 48] if c.isdigit() and c.isascii() else c for c in s)
    if ISO_D.fullmatch(t) and not ISO_A.fullmatch(t):
        admitted += 1
        try:
            date.fromisoformat(t)
            bad += 1  # would be an accepted non-ASCII date
        except ValueError:
            pass
print(f"W4: {admitted} non-ASCII-digit strings admitted by \\d but not by [0-9]; accepted by date.fromisoformat: {bad}")
# length argument for W6
import itertools
lens = set()
for y in range(1, 10000, 997):
    for m in range(1, 13):
        for d in range(1, 29):
            for s in (f"{y:04d}-{m:02d}-{d:02d}", f"{y:04d}{m:02d}{d:02d}"):
                try:
                    date.fromisoformat(s)
                    lens.add(len(s))
                except ValueError:
                    pass
print("W6: lengths of strings date.fromisoformat accepts (YYYY-MM-DD and YYYYMMDD forms, sampled):", sorted(lens))
