import csv
import math
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def load(name: str) -> tuple[list[str], list[str], NDArray[np.float64]]:
    """Dates (or months), column names, and values of data/<name>; NaN where the source has no observation."""
    with (Path("data") / name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    body = rows[1:]
    values = np.array([[float(v) if v else math.nan for v in row[1:]] for row in body])
    return [row[0] for row in body], rows[0][1:], values


print("file rows columns first last missing_cells")
for name in ("fx_daily.csv", "fx_monthly.csv", "ust_daily.csv"):
    keys, columns, values = load(name)
    print(f"{name} {len(keys)} {len(columns)} {keys[0]} {keys[-1]} {int(np.isnan(values).sum())}")

# Month-end FX from the euro's launch: annualised volatility of monthly log changes in USD per unit, percent.
months, currencies, fx = load("fx_monthly.csv")
changes = np.diff(np.log(fx[months.index("1999-01") :]), axis=0)
print(f"currency ann_vol_pct over {len(changes)} months to {months[-1]}")
for currency, vol in zip(currencies, changes.std(axis=0, ddof=1) * math.sqrt(12) * 100, strict=True):
    print(f"{currency} {vol:.2f}")

# 10-year constant-maturity yield minus the 3-month bill rate (discount basis), percentage points.
days, _, ust = load("ust_daily.csv")
both = ~np.isnan(ust).any(axis=1)
spread = ust[both, 1] - ust[both, 0]
print(f"spread_10y_3m mean {spread.mean():.2f} pp, inverted on {100 * (spread < 0).mean():.1f} % of {both.sum()} days")
