"""CF9 lab L06-1: Selective Hedging, Cash-Flow-at-Risk (CFaR), and Hedge Accounting.

Simulates corporate risk governance and treasury execution:
1. Cash-Flow-at-Risk (CFaR) estimation at 95% confidence and shortfall probability below capex hurdle K.
2. Disciplined passive hedge program: variance reduction and elimination of tail shortfall.
3. Selective hedging (managerial market timing): increased tail variance and speculative losses.
4. ASC 815 / IFRS 9 hedge accounting eligibility test (80%-125% dollar-offset corridor).
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def compute_cfar_metrics(
    mean_cf: float,
    std_cf: float,
    confidence: float = 0.95,
    hurdle: float = 65.0,
) -> dict[str, float]:
    """Compute analytical Cash-Flow-at-Risk (CFaR) and shortfall probability below hurdle K."""
    dist = NormalDist()
    z_alpha = dist.inv_cdf(confidence)
    cfar_amount = z_alpha * std_cf
    worst_case_cf = mean_cf - cfar_amount

    # Shortfall probability: Prob(CF < hurdle)
    z_hurdle = (hurdle - mean_cf) / std_cf if std_cf > 0.0 else (-1e9 if mean_cf > hurdle else 1e9)
    prob_shortfall = dist.cdf(z_hurdle)

    return {
        "mean_cf": mean_cf,
        "std_cf": std_cf,
        "cfar_amount": cfar_amount,
        "worst_case_cf": worst_case_cf,
        "prob_shortfall": prob_shortfall,
    }


def evaluate_dollar_offset_ratio(delta_derivative: float, delta_hedged_item: float) -> dict[str, float | bool]:
    """Evaluate retrospective effectiveness under ASC 815 / IFRS 9 (80% - 125% corridor)."""
    if abs(delta_hedged_item) < 1e-9:
        return {"offset_ratio": 0.0, "is_effective": False}

    ratio = abs(delta_derivative) / abs(delta_hedged_item)
    is_effective = 0.80 <= ratio <= 1.25

    return {
        "offset_ratio": ratio,
        "is_effective": is_effective,
    }


def simulate_treasury_policies(
    n_sims: int = 5000,
    mean_cf: float = 100.0,
    sigma_unhedged: float = 25.0,
    hurdle_k: float = 65.0,
) -> dict[str, dict[str, float]]:
    """Compare unhedged, passive hedge, and selective hedge policies."""
    dist = NormalDist()
    probs = [(i + 0.5) / n_sims for i in range(n_sims)]
    z = [dist.inv_cdf(p) for p in probs]

    # 1. Unhedged cash flow: CF = mu + sigma * z
    cf_unhedged = [mean_cf + sigma_unhedged * zi for zi in z]

    # 2. Disciplined Passive Hedge: 80% coverage with 90% correlation instrument
    # Residual volatility ~ sqrt(1 - 0.80^2 * 0.90^2) * sigma ~ 0.35 * 25 ~ 8.75M
    cf_passive = [mean_cf + 8.5 * zi for zi in z]

    # 3. Selective Hedging (manager times the market based on noisy signal)
    # Stulz (1996) and Adam & Fernando (2006): market timing adds speculative variance
    # When z < 0, manager thought market would rise, under-hedged; when z > 0, over-hedged
    cf_selective = [mean_cf + sigma_unhedged * zi + (10.0 * zi if zi < 0.0 else -5.0 * zi) for zi in z]

    def summarize(cfs: list[float]) -> dict[str, float]:
        n = len(cfs)
        m = sum(cfs) / n
        s = math.sqrt(sum((c - m) ** 2 for c in cfs) / (n - 1))
        # 5th percentile empirical worst case
        sorted_cfs = sorted(cfs)
        p5 = sorted_cfs[int(0.05 * n)]
        shortfalls = sum(1 for c in cfs if c < hurdle_k) / n
        return {
            "mean": m,
            "std": s,
            "cfar_95": m - p5,
            "worst_5pct": p5,
            "prob_shortfall": shortfalls,
        }

    return {
        "unhedged": summarize(cf_unhedged),
        "passive": summarize(cf_passive),
        "selective": summarize(cf_selective),
    }


def main() -> None:
    print("CF9 Lab L06-1: Selective Hedging, CFaR & Hedge Accounting")
    print("=========================================================")

    # Analytical CFaR benchmarks
    unhedged_cfar = compute_cfar_metrics(mean_cf=100.0, std_cf=25.0, hurdle=65.0)
    passive_cfar = compute_cfar_metrics(mean_cf=100.0, std_cf=8.5, hurdle=65.0)

    print("1. Analytical Cash-Flow-at-Risk (CFaR 95% Confidence):")
    print(f"   Baseline expected cash flow (E[CF]):  ${unhedged_cfar['mean_cf']:.2f}M")
    print("   Critical hurdle K (Capex + Debt):     $65.00M")
    print(f"   Unhedged 95% CFaR shortfall:          ${unhedged_cfar['cfar_amount']:.2f}M")
    print(f"   Unhedged worst 5% cash flow:          ${unhedged_cfar['worst_case_cf']:.2f}M (< Hurdle: True)")
    print(f"   Unhedged hurdle shortfall risk:       {unhedged_cfar['prob_shortfall']:.2%}")
    print(f"   Passive hedge 95% CFaR:               ${passive_cfar['cfar_amount']:.2f}M")
    print(f"   Passive hedge worst 5% cash flow:     ${passive_cfar['worst_case_cf']:.2f}M (Protection Confirmed)")
    print(f"   Passive hedge shortfall risk:         {passive_cfar['prob_shortfall']:.4%}")

    # Simulated policies
    sims = simulate_treasury_policies()
    print("\n2. Treasury Policy Simulation (5,000 States):")
    for name, s in sims.items():
        print(
            f"   Policy: {name.capitalize():<11} Mean=${s['mean']:<6.2f}M Std=${s['std']:<6.2f}M "
            f"Worst 5%=${s['worst_5pct']:<6.2f}M Shortfall Risk={s['prob_shortfall']:.2%}"
        )

    # Hedge accounting test
    print("\n3. ASC 815 / IFRS 9 Hedge Accounting Compliance (80%-125% Rule):")
    h1 = evaluate_dollar_offset_ratio(delta_derivative=9.5, delta_hedged_item=-10.0)
    h2 = evaluate_dollar_offset_ratio(delta_derivative=14.0, delta_hedged_item=-10.0)
    print(
        f"   Case 1: Deriv = +$9.5M, Exposure = -$10.0M -> "
        f"Offset = {float(h1['offset_ratio']):.2%}, Qualified: {h1['is_effective']}"
    )
    print(
        f"   Case 2: Deriv = +$14.0M, Exposure = -$10.0M -> "
        f"Offset = {float(h2['offset_ratio']):.2%}, Qualified: {h2['is_effective']}"
    )


main()
