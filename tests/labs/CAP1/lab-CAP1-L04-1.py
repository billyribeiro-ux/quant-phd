"""Lab 4: Empirical divergence decomposition and step-by-step waterfall auditor."""

from __future__ import annotations


def decompose_divergences(stages: dict[str, float]) -> list[tuple[str, float, float, float]]:
    stage_keys = list(stages.keys())
    base_val = stages[stage_keys[0]]
    results: list[tuple[str, float, float, float]] = []

    for i, key in enumerate(stage_keys):
        val = stages[key]
        delta_step = 0.0 if i == 0 else val - stages[stage_keys[i - 1]]
        delta_cumulative = val - base_val
        results.append((key, val, delta_step, delta_cumulative))

    return results


def main() -> None:
    # Tracking gross profitability or momentum spread return across pipeline variations
    pipeline_steps = {
        "0. Published Paper (Reported Table)": 0.840,
        "1. Raw Unfiltered Sample": 0.950,
        "2. Ordinary Common Share Filter (SHRCD 10/11)": 0.820,
        "3. Shumway (1997) Delisting Imputation": 0.650,
        "4. Cross-Sectional Winsorization (1%/99%)": 0.620,
        "5. Value-Weighted Portfolio (Replicated Benchmark)": 0.440,
    }

    waterfall = decompose_divergences(pipeline_steps)

    print(f"{'Pipeline Stage':<50} | {'Spread (%)':<10} | {'Step Delta':<10} | {'Cumulative':<10}")
    print("-" * 88)
    for stage, val, step, cum in waterfall:
        print(f"{stage:<50} | {val:>10.3f} | {step:>+10.3f} | {cum:>+10.3f}")

    vw_target = pipeline_steps["5. Value-Weighted Portfolio (Replicated Benchmark)"]
    pub_target = pipeline_steps["0. Published Paper (Reported Table)"]
    total_wedge = vw_target - pub_target
    print("-" * 88)
    print(f"Total Divergence Wedge: {total_wedge:+.3f}% per month ({total_wedge * 12:+.2f}% annualized)")
    print("Primary drivers: Shumway delisting (-0.170%) and Value-weighting (-0.180%)")


main()
