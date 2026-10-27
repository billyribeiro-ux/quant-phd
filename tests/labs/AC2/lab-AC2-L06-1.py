"""AC2 L06 lab 1: the modified Jones model on a SIMULATED cross-section with a planted manipulation.

SIMULATED: every firm-year is generated here from the seeded model below. No filing is read.
The manipulation is planted by the author: a known share of firms receives a positive discretionary
accrual of SHIFT times lagged assets. The lab asks whether the regression recovers it, and reports
the limits of that recovery. A flagged firm in this lab is a firm the generator made manipulate.
In real data, a large discretionary accrual is evidence of a candidate, not of intent.

Model, per firm i (all money in currency units, CU; ratios are per unit of lagged assets):
    lag_i     lagged total assets, lognormal around 1000 CU
    drev_i    change in revenue, drec_i change in receivables
    ppe_i     net PP&E
    total_i   total accruals = C1 / lag + C2 * (drev - drec) / lag + C3 * ppe / lag + DA_i
    DA_i      = SHIFT * manipulator_i + NOISE_SD * v_i,  v_i iid N(0, 1)

The estimator is the A15 contract's modified_jones: regress total/lag on
[1/lag, (drev - drec)/lag, ppe/lag] WITHOUT an intercept, by least squares (numpy lstsq, rcond=None).
Its fitted values are the nondiscretionary accruals and its residuals the discretionary accruals.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

F64 = NDArray[np.float64]

N_FIRMS = 2000
MANIP_SHARE = 0.10  # share of firm-years that manipulate, planted
C_TRUE = (0.05, 0.10, -0.08)  # planted coefficients of the nondiscretionary part, on 1/lag, (drev-drec)/lag, ppe/lag
NOISE_SD = 0.01  # normal discretionary variation, ratio to lagged assets
SEED = 606


@dataclass(frozen=True)
class Sample:
    """A cross-section of firm-years: money in CU, manipulator flags are the planted truth."""

    total: F64
    lag: F64
    drev: F64
    drec: F64
    ppe: F64
    manipulator: NDArray[np.bool_]


def make_sample(seed: int, shift: float, n: int = N_FIRMS) -> Sample:
    """Generate n firm-years; shift is the planted discretionary accrual of a manipulator, in ratio units."""
    rng = np.random.default_rng(seed)
    lag = np.exp(rng.normal(np.log(1000.0), 0.6, n))
    drev = lag * rng.normal(0.10, 0.20, n)
    drec = drev * rng.uniform(0.10, 0.30, n) + lag * rng.normal(0.0, 0.02, n)
    ppe = lag * rng.uniform(0.20, 0.60, n)
    manipulator = np.zeros(n, dtype=np.bool_)
    manipulator[rng.permutation(n)[: round(MANIP_SHARE * n)]] = True
    noise = rng.standard_normal(n)
    da = shift * manipulator + NOISE_SD * noise
    nondiscretionary = C_TRUE[0] / lag + C_TRUE[1] * (drev - drec) / lag + C_TRUE[2] * ppe / lag
    total = lag * (nondiscretionary + da)
    return Sample(total=total, lag=lag, drev=drev, drec=drec, ppe=ppe, manipulator=manipulator)


def design(s: Sample) -> tuple[F64, F64]:
    """Regressors [1/lag, (drev - drec)/lag, ppe/lag] and the dependent variable total/lag, one row per firm-year."""
    x = np.column_stack([1.0 / s.lag, (s.drev - s.drec) / s.lag, s.ppe / s.lag])
    return x, s.total / s.lag


def modified_jones(s: Sample, mask: NDArray[np.bool_] | None = None) -> tuple[tuple[float, float, float], F64, F64]:
    """A15 contract's modified_jones on the rows selected by mask (all rows if None).

    Returns the coefficients (a1, a2, a3), the fitted nondiscretionary accruals and the discretionary accruals
    (total/lag minus fitted) for every row of the sample, all in ratio units of lagged assets.
    """
    keep = np.ones(s.lag.size, dtype=np.bool_) if mask is None else mask
    x, y = design(s)
    coef, *_ = np.linalg.lstsq(x[keep], y[keep], rcond=None)
    fitted = x @ coef
    return (float(coef[0]), float(coef[1]), float(coef[2])), fitted, y - fitted


def classical_se(s: Sample, mask: NDArray[np.bool_]) -> F64:
    """Classical OLS standard errors of (a1, a2, a3) on the rows in mask, with iid errors assumed."""
    x, y = design(s)
    xk, yk = x[mask], y[mask]
    coef, *_ = np.linalg.lstsq(xk, yk, rcond=None)
    resid = yk - xk @ coef
    s2 = float(resid @ resid) / (yk.size - xk.shape[1])
    return np.sqrt(np.diag(s2 * np.linalg.inv(xk.T @ xk)))


def report(label: str, s: Sample) -> None:
    """Estimate on all firm-years (the practical case) and on the non-manipulators (an oracle, not available)."""
    (a1, a2, a3), _, da = modified_jones(s)
    print(f"{label} coefficients_all_firms {a1:.4f} {a2:.4f} {a3:.4f}")
    (o1, o2, o3), _, da_oracle = modified_jones(s, ~s.manipulator)
    print(f"{label} coefficients_non_manipulators {o1:.4f} {o2:.4f} {o3:.4f}")
    se = classical_se(s, ~s.manipulator)
    print(f"{label} se_non_manipulators {se[0]:.4f} {se[1]:.4f} {se[2]:.4f}")
    print(f"{label} planted_coefficients {C_TRUE[0]:.4f} {C_TRUE[1]:.4f} {C_TRUE[2]:.4f}")

    m = s.manipulator
    print(f"{label} mean_da_manipulators {float(da[m].mean()):.4f} mean_da_others {float(da[~m].mean()):.4f}")

    # Flag the 10% of firm-years with the largest discretionary accruals, the same share as the planted one.
    cut = float(np.quantile(da, 1.0 - MANIP_SHARE))
    flagged = da >= cut
    tpr = float(np.mean(flagged[m]))
    fpr = float(np.mean(flagged[~m]))
    print(f"{label} all_firms_top10pct true_positive_rate {tpr:.4f} false_positive_rate {fpr:.4f}")

    cut_o = float(np.quantile(da_oracle, 1.0 - MANIP_SHARE))
    flagged_o = da_oracle >= cut_o
    print(
        f"{label} oracle_top10pct true_positive_rate {float(np.mean(flagged_o[m])):.4f} "
        f"false_positive_rate {float(np.mean(flagged_o[~m])):.4f}"
    )
    print(f"{label} flags_differing_all_vs_oracle {int(np.sum(flagged != flagged_o))}")


SCALE_SEEDS = (606, 607, 608, 609, 610)


def se_scaling() -> None:
    """Mean classical standard error of a1 on the non-manipulators, over SCALE_SEEDS, at two sample sizes."""
    for n in (2000, 64000):
        ses: list[float] = []
        for seed in SCALE_SEEDS:
            sample = make_sample(seed, 0.05, n)
            ses.append(classical_se(sample, ~sample.manipulator)[0])
        print(f"a1_se_mean firms {n} seeds {len(SCALE_SEEDS)} {float(np.mean(ses)):.4f}")


def main() -> None:
    print(f"seed {SEED} firms {N_FIRMS} manipulator_share {MANIP_SHARE}")
    report("strong_shift_0.05", make_sample(SEED, 0.05))
    report("weak_shift_0.01", make_sample(SEED, 0.01))
    se_scaling()


if __name__ == "__main__":
    main()
