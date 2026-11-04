import csv, math
from decimal import Decimal, getcontext
getcontext().prec = 60
rows = [(r["month"], Decimal(r["GBP"])) for r in csv.DictReader(open("/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline=""))]
ch = [(m, (v / p).ln()) for (_, p), (m, v) in zip(rows, rows[1:])]
for start in ("1990-01", "2000-01", "2010-01"):
    w = [c for m, c in ch if m >= start]
    n = len(w); mu = sum(w) / n
    sd = (sum((x - mu) ** 2 for x in w) / (n - 1)).sqrt()
    print(start, n, round(float(sd), 6))
