"""Smallest nonzero monthly log change in the GBP column, and the count of changes below 1e-6 in absolute value (for mutant r12n03)."""
import csv
import math
from fractions import Fraction as F

rows = list(csv.DictReader(open("course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
gbp = [(r["month"], F(r["GBP"])) for r in rows]
logs = [(m, math.log(float(r / p))) for (_, p), (m, r) in zip(gbp, gbp[1:])]
nonzero = [abs(v) for _, v in logs if v != 0.0]
print("changes", len(logs), "exact zeros", sum(v == 0.0 for _, v in logs))
print("smallest nonzero |change|", min(nonzero), "count below 1e-6 (nonzero)", sum(1 for x in nonzero if x < 1e-6), "count below 1e-4", sum(1 for x in nonzero if x < 1e-4))
