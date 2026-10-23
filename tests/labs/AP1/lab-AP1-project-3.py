import csv
import math
from pathlib import Path

import numpy as np

# The report's data: nine one-month currency payoffs, each costing one dollar (DKK left out: Lesson 1, Lab 2).
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, months = rows[0][1:], [row[0] for row in rows[1:]]
rates = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(rates).any(axis=1)))  # first month with a rate for every currency
keep = [i for i, c in enumerate(currencies) if c != "DKK"]
names = [currencies[i] for i in keep]
x = rates[start + 1 :, keep] / rates[start:-1, keep]  # (T, 9): dollars received per dollar of currency held
ends = months[start + 1 :]  # the month in which each payoff is received
prices = np.ones(len(keep))
half = x.shape[0] // 2
train, test = x[:half], x[half:]
print(f"payoffs: {', '.join(names)}")
print(f"train {ends[0]} to {ends[half - 1]} ({half} months); test {ends[half]} to {ends[-1]} ({len(test)} months)")
print(f"checksums: sum {x.sum():.10f} sum of squares {(x**2).sum():.10f}")

b = np.linalg.solve(train.T @ train / half, prices)
m_train, m_test = train @ b, test @ b
in_err = train.T @ m_train / half - prices
out_err = test.T @ m_test / len(test) - prices
print(f"max |in-sample error|: {np.abs(in_err).max():.1e}")
print("out-of-sample errors (bp):", " ".join(f"{c} {1e4 * e:.1f}" for c, e in zip(names, out_err, strict=True)))
print(f"out-of-sample rms: {1e4 * np.sqrt(np.mean(out_err**2)):.1f} bp")
print(f"x* on train: mean {m_train.mean():.4f}, s.d. {m_train.std():.4f}")
print(f"x* on test: share negative {np.mean(m_test < 0):.4f}, min {m_test.min():.4f}")
print(f"benchmark m = 1, test rms: {1e4 * np.sqrt(np.mean((test.mean(axis=0) - prices) ** 2)):.1f} bp")
