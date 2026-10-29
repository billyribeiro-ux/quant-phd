"""Write ten student-error mutants of the CF1 reference into ledgers/CF1/mutants/ (fx19d01 to fx19d10).

Each mutant is the reference with exactly one replacement, each asserted to match once. The first line of the
module docstring names the error, as mutate_graders.py reads it.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
REFERENCE = ROOT / "course/modules/CF/CF1/grader/reference.py"
OUT = ROOT / "ledgers/CF1/mutants"

MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "fx19d01_rate_check_accepts_exactly_minus_one",
        "NPV accepts a rate of exactly -1, where the discount factor is undefined.",
        "    if not _finite(rate) or rate <= -1.0:",
        "    if not _finite(rate) or rate < -1.0:",
    ),
    (
        "fx19d02_npv_of_empty_flows_is_zero",
        "NPV of an empty list of flows returns zero instead of refusing the request.",
        "    if len(flows) == 0:\n"
        '        raise ValueError("flows is empty: a project with no cash flows has no value to discount")\n',
        "",
    ),
    (
        "fx19d03_irr_accepts_a_single_flow",
        "An IRR request with one flow is accepted, so the fewer-than-two-flows rule is off by one.",
        '    if len(flows) < 2:\n        raise ValueError("irr_roots needs at least an outlay and one inflow")',
        '    if len(flows) < 1:\n        raise ValueError("irr_roots needs at least an outlay and one inflow")',
    ),
    (
        "fx19d04_irr_refuses_a_positive_first_flow",
        "An IRR request whose first flow is positive is refused, as if the outlay had to come first.",
        "    if all(cf == 0 for cf in flows):\n"
        '        raise ValueError("every flow is zero: then every rate is a root, and the question has no answer")\n',
        "    if all(cf == 0 for cf in flows):\n"
        '        raise ValueError("every flow is zero: then every rate is a root, and the question has no answer")\n'
        '    if flows[0] > 0:\n        raise ValueError("the first flow must be an outlay")\n',
    ),
    (
        "fx19d05_tax_rate_of_zero_refused",
        "A tax rate of exactly zero is refused: the lower bound is treated as exclusive.",
        "    if not _finite(tax_rate) or not 0.0 <= tax_rate < 1.0:",
        "    if not _finite(tax_rate) or not 0.0 < tax_rate < 1.0:",
    ),
    (
        "fx19d06_working_capital_share_of_one_accepted",
        "A working-capital share of exactly 100 percent is accepted: the upper bound is treated as inclusive.",
        "    if not _finite(share) or not 0.0 <= share < 1.0:",
        "    if not _finite(share) or not 0.0 <= share <= 1.0:",
    ),
    (
        "fx19d07_boolean_capex_accepted",
        "A capex given as a boolean is accepted, because the check does not exclude bool.",
        "    if not isinstance(capex, int) or isinstance(capex, bool) or capex <= 0:",
        "    if not isinstance(capex, int) or capex <= 0:",
    ),
    (
        "fx19d08_volatility_just_below_zero_accepted",
        "A negative volatility of -1e-12 is accepted, because the check tolerates a tiny negative value.",
        "    if not _finite(volatility) or volatility < 0.0:",
        "    if not _finite(volatility) or volatility < -1e-9:",
    ),
    (
        "fx19d09_first_payback_flow_of_minus_1e9_refused",
        "A payback whose first flow is -1e-9 cents is refused, because the outlay test uses a tolerance.",
        "    if not flows[0] < 0:",
        "    if not flows[0] < -1e-9:",
    ),
    (
        "fx19d10_inflation_of_minus_one_accepted_in_a_project",
        "A project with inflation of exactly -1 is accepted: the inflation check is strict.",
        "    if not _finite(inflation) or inflation <= -1.0:",
        "    if not _finite(inflation) or inflation < -1.0:",
    ),
]


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    end = source.index('"""', 3) + 3
    body = source[end:]
    for name, description, old, new in MUTANTS:
        count = body.count(old)
        assert count == 1, f"{name}: the target text occurs {count} times"
        mutated = body.replace(old, new)
        header = f'"""{description}\n\nMutant {name}.\n"""'
        (OUT / f"{name}.py").write_text(header + mutated, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
