"""Blank cells per column of fx_monthly.csv, first non-blank month per column, and the hub's data claims."""
import csv
rows = list(csv.reader(open("/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a/course/assets/data/market/fx_monthly.csv", encoding="utf-8")))
hdr, data = rows[0], rows[1:]
print("rows", len(data), "first", data[0][0], "last", data[-1][0])
for i, c in enumerate(hdr[1:], start=1):
    blanks = sum(1 for r in data if r[i].strip() == "")
    first = next((r[0] for r in data if r[i].strip() != ""), None)
    print(c, "blanks", blanks, "first non-blank", first)
import json
man = json.load(open("/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a/course/assets/data/market/MANIFEST.json", encoding="utf-8"))
print("MANIFEST ids:", [x["id"] for x in man["datasets"]])
