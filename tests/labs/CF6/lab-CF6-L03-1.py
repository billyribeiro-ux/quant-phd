"""CF6 Lesson 3 Inline Lab 1: Long-Run IPO Performance (BHAR & Wealth Relative).

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
"""

from __future__ import annotations

import random


def compute_bhar(
    firm_rets: list[float],
    bench_rets: list[float],
) -> dict[str, float]:
    n = len(firm_rets)
    prod_f = 1.0
    prod_b = 1.0
    car = 0.0
    for rf, rb in zip(firm_rets, bench_rets, strict=True):
        prod_f *= 1.0 + rf
        prod_b *= 1.0 + rb
        car += rf - rb

    bhar = prod_f - prod_b
    wr = prod_f / prod_b if prod_b != 0.0 else 0.0
    ann_f = (prod_f ** (12.0 / float(n))) - 1.0
    ann_b = (prod_b ** (12.0 / float(n))) - 1.0

    return {
        "bhar": bhar,
        "wealth_relative": wr,
        "car": car,
        "firm_compounded": prod_f - 1.0,
        "benchmark_compounded": prod_b - 1.0,
        "annualized_abnormal": ann_f - ann_b,
    }


def main() -> None:
    # Seeded simulation matching Ritter (1991) and Loughran & Ritter (1995) empirical findings
    # 36 monthly returns for an IPO cohort vs matching style benchmark
    rng = random.Random(42)
    n_months = 36

    # Simulated IPO returns: initial year positive, subsequent 2 years underperforming
    # Ritter (1991) 3-year cumulative returns: ~34.5% IPO vs ~61.9% matching firm
    ipo_returns = [round(rng.gauss(0.008, 0.055), 4) for _ in range(n_months)]
    bench_returns = [round(rng.gauss(0.013, 0.038), 4) for _ in range(n_months)]

    res = compute_bhar(ipo_returns, bench_returns)

    print("=== 36-Month Long-Run Performance Evaluation ===")
    print(f"IPO 36-Month Compound Return:       {res['firm_compounded'] * 100:.2f}%")
    print(f"Benchmark 36-Month Compound Return: {res['benchmark_compounded'] * 100:.2f}%\n")
    print(f"Buy-and-Hold Abnormal Return (BHAR): {res['bhar'] * 100:.2f}%")
    print(f"Cumulative Abnormal Return (CAR):    {res['car'] * 100:.2f}%")
    print(f"Ritter Wealth Relative (WR):         {res['wealth_relative']:.4f}")
    print(f"Annualized Abnormal Geometric Return:{res['annualized_abnormal'] * 100:.2f}%/year\n")

    # Bootstrap test of H0: BHAR >= 0
    n_boot = 1_000
    boot_diffs = []
    diffs = [f - b for f, b in zip(ipo_returns, bench_returns, strict=True)]
    for _ in range(n_boot):
        sample = [rng.choice(diffs) for _ in range(n_months)]
        boot_diffs.append(sum(sample))

    p_value = sum(1 for d in boot_diffs if d >= 0) / float(n_boot)
    print(f"Bootstrap Test of Zero Abnormal Performance (p-value): {p_value:.3f}")
    if p_value < 0.05:
        print("Verdict: Reject null of market efficiency; significant long-run IPO underperformance.")
    else:
        print("Verdict: Cannot reject null of market efficiency at 5% level.")


main()
