"""Round-17 verifier: independent checks of the embedded snapshot used by project Lab 3 and the page's data claims.

Usage: python -I data_checks_r17.py <checkout_root>. Reads course/assets/data/market/fx_monthly.csv and MANIFEST.json.
Uses only the csv, hashlib and json modules; it does not import the lab code.
"""
import csv
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
csv_path = root / "course/assets/data/market/fx_monthly.csv"
raw = csv_path.read_bytes()
man = json.loads((root / "course/assets/data/market/MANIFEST.json").read_text(encoding="utf-8"))
DS = {d["id"]: d for d in man["datasets"]}
entry = DS["fx_monthly"]
print("sha256 file:", hashlib.sha256(raw).hexdigest(), "manifest:", entry["sha256"], "match:", hashlib.sha256(raw).hexdigest() == entry["sha256"])
rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
print("rows:", len(rows), "first:", rows[0]["month"], "last:", rows[-1]["month"], "manifest rows:", entry["rows"])
print("columns:", list(rows[0].keys())[1:], "manifest columns match:", list(rows[0].keys())[1:] == entry["columns"])
blank_gbp = [r["month"] for r in rows if r["GBP"].strip() == ""]
print("blank GBP cells:", len(blank_gbp))
eur = [r["month"] for r in rows if r["EUR"].strip() != ""]
print("EUR first non-blank:", eur[0], "last blank EUR month:", [r["month"] for r in rows if r["EUR"].strip() == ""][-1])
blank_eur_before_1999 = all(r["EUR"] == "" for r in rows if r["month"] < "1999-01")
print("EUR blank for every month before 1999-01:", blank_eur_before_1999)
print("interest-rate columns present:", any(k in rows[0] for k in ("tbill_3m", "cmt_10y", "rate")))
# month continuity
def idx(m):
    y, mm = m.split("-")
    return int(y) * 12 + int(mm) - 1
gaps = [(a["month"], b["month"]) for a, b in zip(rows, rows[1:]) if idx(b["month"]) != idx(a["month"]) + 1]
print("month gaps:", gaps)
print("transform inverts:", [c for c in entry["transform"].split("inverted")[0].split(";")[-1].split(",")])
print("GBP transform text:", "GBP" in entry["transform"].split("inverted")[0], "GBP in inverted list:", "GBP" in entry["transform"].split("inverted to")[0].split("inverted")[0])
print("title:", entry["title"])
print("licence:", entry["licence"])
print("retrieved:", entry["retrieved"])
other = ["fx_daily", "ust_daily"]
print("MANIFEST datasets:", sorted(DS))
for k in other:
    print(k, "title:", DS[k]["title"])
