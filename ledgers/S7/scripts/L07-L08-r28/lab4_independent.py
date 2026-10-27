"""Round 28 independent recomputation of S7 L08 Lab 4 (PBO and DSR on 40 currency sign rules), written from the
text of the lesson, not from the lab twin. Reads the committed snapshot course/assets/data/market/fx_monthly.csv.
Deterministic part: the 40 trials, Sharpe ratios, PSR, DSR, the effective number, PBO at S = 8, 10 and 16.
Null part: 100 grids on months resampled with replacement, numpy default_rng(4008) (the lab's seed), as the page says.
Run: .venv/bin/python -I <this file> <path to fx_monthly.csv>
"""

from __future__ import annotations

import csv
import itertools
import math
import sys
from statistics import NormalDist

import numpy as np

PHI = NormalDist()
GAMMA = 0.5772156649015329


def bracket(n: float) -> float:
    return (1 - GAMMA) * PHI.inv_cdf(1 - 1 / n) + GAMMA * PHI.inv_cdf(1 - 1 / (n * math.e))


def load(path: str) -> tuple[list[str], list[str], np.ndarray]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    currencies = rows[0][1:]
    months = [r[0] for r in rows[1:]]
    prices = np.array([[float(v) if v != "" else np.nan for v in r[1:]] for r in rows[1:]])
    return currencies, months, prices


def trials_direct(log_p: np.ndarray, first: int, grid: list[tuple[int, int, int]]) -> np.ndarray:
    """Monthly spot return series of each rule, built month by month (no cumulative-sum shortcut)."""
    n_months = log_p.shape[0]
    spot = np.exp(np.diff(log_p, axis=0)) - 1.0  # spot[k] = return over month k + 1
    out = np.zeros((n_months - first, len(grid)))
    for k, (lb, hold, skip) in enumerate(grid):
        for idx, t in enumerate(range(first, n_months)):
            weights = np.zeros(log_p.shape[1])
            for h in range(1, hold + 1):
                formed = t - h - skip
                weights += np.sign(log_p[formed] - log_p[formed - lb])
            weights = weights / hold
            out[idx, k] = float(np.mean(weights * spot[t - 1]))
    return out


def sharpe_cols(x: np.ndarray) -> np.ndarray:
    return x.mean(axis=0) / x.std(axis=0, ddof=1)


def pbo(m: np.ndarray, s: int) -> float:
    """CSCV PBO by direct enumeration with block sums (Sharpe via sums; ranks with average ties)."""
    m = m[m.shape[0] % s :]
    size = m.shape[0] // s
    blocks = m.reshape(s, size, m.shape[1])
    b1 = blocks.sum(axis=1)
    b2 = (blocks**2).sum(axis=1)
    half = s // 2
    logits = []
    for combo in itertools.combinations(range(s), half):
        out_idx = [b for b in range(s) if b not in combo]
        n_in, n_out = half * size, (s - half) * size
        s1i, s2i = b1[list(combo)].sum(axis=0), b2[list(combo)].sum(axis=0)
        s1o, s2o = b1[out_idx].sum(axis=0), b2[out_idx].sum(axis=0)
        mi = s1i / n_in
        mo = s1o / n_out
        sri = mi / np.sqrt((s2i - n_in * mi**2) / (n_in - 1))
        sro = mo / np.sqrt((s2o - n_out * mo**2) / (n_out - 1))
        best = int(np.argmax(sri))
        lower = np.sum(sro < sro[best])
        equal = np.sum(sro == sro[best])
        rank = 1 + lower + 0.5 * (equal - 1)
        omega = rank / (m.shape[1] + 1)
        logits.append(math.log(omega / (1 - omega)))
    return float(np.mean(np.array(logits) <= 0))


def psr(r: np.ndarray, bench: float) -> float:
    n = r.size
    sr = r.mean() / r.std(ddof=1)
    c = r - r.mean()
    m2, m3, m4 = (np.mean(c**k) for k in (2, 3, 4))
    g3, g4 = m3 / m2**1.5, m4 / m2**2
    se = math.sqrt((1 - g3 * sr + (g4 - 1) / 4 * sr**2) / (n - 1))
    return PHI.cdf((sr - bench) / se)


def main() -> None:
    currencies, months, prices = load(sys.argv[1])
    start = int(np.argmax(~np.isnan(prices).any(axis=1)))
    months, log_p = months[start:], np.log(prices[start:])
    grid = list(itertools.product((1, 3, 6, 9, 12), (1, 3, 6, 12), (0, 1)))
    first = max(h for _, h, _ in grid) + max(s for _, _, s in grid) + max(lb for lb, _, _ in grid)
    trials = trials_direct(log_p, first, grid)
    n_obs, n_tr = trials.shape
    srs = sharpe_cols(trials)
    pick = int(np.argmax(srs))
    sel = trials[:, pick]
    print(f"[ind] months {len(months)} from {months[0]} to {months[-1]}; window {months[first]} to {months[-1]} n_obs {n_obs} N {n_tr}")
    print(f"[ind] annualized Sharpe min {srs.min() * math.sqrt(12):.3f} median {np.median(srs) * math.sqrt(12):.3f}")
    print(f"[ind] best L{grid[pick][0]}-H{grid[pick][1]}-skip{grid[pick][2]} monthly SR {sel.mean() / sel.std(ddof=1):.4f}")
    print(f"[ind] PSR0 {psr(sel, 0.0):.4f}")
    spread = math.sqrt(float(np.var(srs, ddof=1)))
    sr0 = spread * bracket(n_tr)
    print(f"[ind] cross-sectional sd {spread:.6f} SR0 {sr0:.6f} DSR {psr(sel, sr0):.4f}")
    corr = np.corrcoef(trials, rowvar=False)
    rho = float(corr[~np.eye(n_tr, dtype=bool)].mean())
    ev = np.linalg.eigvalsh(corr)
    pr = float(ev.sum() ** 2 / (ev**2).sum())
    print(f"[ind] mean rho {rho:.4f} participation {pr:.4f}")
    target = math.sqrt(1 - rho) * bracket(n_tr)
    lo, hi = 1.0 + 1e-9, float(n_tr)
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if bracket(mid) < target else (lo, mid)
    n_eff = (lo + hi) / 2
    print(f"[ind] matching N_eff {n_eff:.4f}")
    print(f"[ind] sqrt((1-rho)/T) {math.sqrt((1 - rho) / n_obs):.5f}")
    sr0e = bracket(n_eff) / math.sqrt(n_obs)
    print(f"[ind] SR0 with N_eff and 1/T {sr0e:.5f} DSR {psr(sel, sr0e):.4f}")
    for s in (8, 10, 16):
        print(f"[ind] PBO S={s}: {pbo(trials, s):.4f}")
    rng = np.random.default_rng(4008)
    changes = np.diff(log_p, axis=0)
    pbo_null, dsr_null = [], []
    for _ in range(100):
        draw = changes[rng.integers(0, len(changes), size=len(changes))]
        path = np.vstack([log_p[:1], log_p[0] + np.cumsum(draw, axis=0)])
        tr = trials_direct(path, first, grid)
        srn = sharpe_cols(tr)
        hurdle = math.sqrt(float(np.var(srn, ddof=1))) * bracket(n_tr)
        pbo_null.append(pbo(tr, 16))
        dsr_null.append(psr(tr[:, int(np.argmax(srn))], hurdle))
    pbo_null_a, dsr_null_a = np.array(pbo_null), np.array(dsr_null)
    obs16 = pbo(trials, 16)
    print(f"[ind] null PBO mean {pbo_null_a.mean():.3f} sd {pbo_null_a.std(ddof=1):.3f} share>= {obs16:.4f}: {np.mean(pbo_null_a >= obs16):.3f}")
    print(f"[ind] null DSR median {np.median(dsr_null_a):.3f} share>= {psr(sel, sr0):.4f}: {np.mean(dsr_null_a >= psr(sel, sr0)):.3f}")


if __name__ == "__main__":
    main()
