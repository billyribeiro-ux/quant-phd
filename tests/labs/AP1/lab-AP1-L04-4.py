import csv
import math
from pathlib import Path

import numpy as np

# The sample x* of nine one-month currency payoffs, each costing one dollar (DKK left out, Lesson 1).
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies = rows[0][1:]
prices = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(prices).any(axis=1)))
keep = [i for i, c in enumerate(currencies) if c != "DKK"]
x = prices[start + 1 :, keep] / prices[start:-1, keep]  # (T, 9) payoffs, each with price 1
n_obs = x.shape[0]
b = np.linalg.solve(x.T @ x / n_obs, np.ones(x.shape[1]))
m = x @ b
print(f"T = {n_obs}; E_T[x* x] - 1 for every currency: max abs {np.abs(x.T @ m / n_obs - 1).max():.1e}")
print(f"x*: mean {m.mean():.4f}, s.d. {m.std():.4f}, min {m.min():.4f}, max {m.max():.4f}")
print("weights b:", np.round(b, 2))
