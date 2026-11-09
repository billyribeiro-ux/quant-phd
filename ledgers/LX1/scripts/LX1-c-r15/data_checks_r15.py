"""Round-15 verifier: data facts cited by the project page, read from the embedded files (no lab code).

Usage: python -I data_checks_r15.py <checkout_root>."""
import csv
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
rows = list(csv.DictReader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="")))
print("fx_monthly header:", list(rows[0].keys()))
print("rows:", len(rows), "first:", rows[0]["month"], "last:", rows[-1]["month"])
eur_blank = [r["month"] for r in rows if r["EUR"] == ""]
eur_full = [r["month"] for r in rows if r["EUR"] != ""]
print("EUR blank rows:", len(eur_blank), "first blank:", eur_blank[0], "last blank:", eur_blank[-1])
print("EUR first non-blank:", eur_full[0], "non-blank rows:", len(eur_full))
print("GBP blank cells:", sum(1 for r in rows if r["GBP"] == ""))
months = [r["month"] for r in rows]
def idx(m):
    y, mo = map(int, m.split("-"))
    return y * 12 + mo - 1
print("contiguous months:", all(idx(b) == idx(a) + 1 for a, b in zip(months, months[1:])))
man = json.loads((root / "course/assets/data/market/MANIFEST.json").read_text(encoding="utf-8"))
for d in man["datasets"]:
    print("MANIFEST", d["id"], "|", d["first"], "to", d["last"], "| rows", d["rows"], "| retrieved", d["retrieved"],
          "| sha256", d["sha256"][:16], "| licence_url", d["licence_url"])
    print("   title:", d["title"])
print("interest-rate columns in fx_monthly:", [c for c in rows[0].keys() if "tbill" in c or "cmt" in c or "rate" in c.lower()])
