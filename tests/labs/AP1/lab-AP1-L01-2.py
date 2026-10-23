import csv
import math
from pathlib import Path

import numpy as np

# Month-end spot rates, USD per unit of foreign currency (Federal Reserve H.10 noon buying rates in New York).
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, months = rows[0][1:], [row[0] for row in rows[1:]]
prices = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(prices).any(axis=1)))  # first month with a rate for every currency

# Asset n: one dollar of currency n held as cash for a month. Price 1 dollar; payoff S[t+1]/S[t] dollars.
gross = prices[start + 1 :] / prices[start:-1]
n_obs, n_assets = gross.shape
print(f"{n_obs} monthly payoffs, {months[start + 1]} to {months[-1]}, {n_assets} currencies")

second = gross.T @ gross / n_obs  # sample second-moment matrix E_T[x x']
eigvals = np.linalg.eigvalsh(second)
print(f"eigenvalues of E_T[x x']: smallest {eigvals[0]:.3e}, next {eigvals[1]:.3e}, largest {eigvals[-1]:.4f}")
print(f"condition number: {eigvals[-1] / eigvals[0]:.4g}")

# Which payoffs nearly coincide? Regress the DKK payoff on the EUR payoff and a constant.
dkk, eur = gross[:, currencies.index("DKK")], gross[:, currencies.index("EUR")]
design = np.column_stack([np.ones(n_obs), eur])
coef, *_ = np.linalg.lstsq(design, dkk, rcond=None)
resid = dkk - design @ coef
print(f"DKK on EUR: slope {coef[1]:.4f}, R^2 {1 - resid.var() / dkk.var():.5f}")
print(f"monthly s.d. of the DKK payoff {1e4 * dkk.std():.1f} bp; of the residual {1e4 * resid.std():.2f} bp")
print(f"E_T[(DKK - EUR)^2] / 2 = {np.mean((dkk - eur) ** 2) / 2:.3e}  (Rayleigh quotient of u = (1, -1) / sqrt 2)")

# Without DKK the second-moment matrix is far better conditioned.
keep = [i for i, c in enumerate(currencies) if c != "DKK"]
eig9 = np.linalg.eigvalsh(second[np.ix_(keep, keep)])
print(f"without DKK: smallest eigenvalue {eig9[0]:.3e}, condition number {eig9[-1] / eig9[0]:.4g}")

# The near-redundancy is stable: the same regression before and after 2009-01.
ends = months[start + 1 :]  # month in which each payoff is received
for label, mask in (
    ("1999-02 to 2008-12", np.array([m < "2009-01" for m in ends])),
    ("2009-01 to 2026-09", np.array([m >= "2009-01" for m in ends])),
):
    y, x = dkk[mask], eur[mask]
    sub = np.column_stack([np.ones(y.size), x])
    b, *_ = np.linalg.lstsq(sub, y, rcond=None)
    e = y - sub @ b
    r2 = 1 - e.var() / y.var()
    print(f"{label}: {y.size} months, slope {b[1]:.4f}, R^2 {r2:.5f}, residual s.d. {1e4 * e.std():.2f} bp")
