"""Write five new verifier mutants (round 3) as full modules derived from the grader's reference.py by one edit each."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC3-CF8-c")
REF = (ROOT / "course/modules/CF/CF8/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CF8/mutants"  # r3-04 was moved to ledgers/CF8/equivalent/ after the equivalence argument

EDITS = {
    "r3-01-opex-paid-on-payment-lag": (
        "Opex is paid on the payment lag, like purchases, instead of in its own week.",
        '    return purchases + int(case["weekly_opex_cents"][week - 1])',
        '    return purchases + _half_up(_week_total([int(x) for x in case["weekly_opex_cents"]], case["payment_lag_days"], week))',
    ),
    "r3-02-liquidity-on-start-drawn": (
        "Week-end liquidity uses the drawn balance from the start of the week, so the week's draw or repay is left out.",
        '        liquidity = cash + commitment - drawn\n',
        '        liquidity = cash + commitment - (drawn - draw + repay)\n',
    ),
    "r3-03-pinch-skips-week-13": (
        "The pinch search covers weeks 1 to 12 only, an off-by-one in the range of the search.",
        '    best = min(range(HORIZON), key=lambda i: (rows[i]["headroom_cents"], i))',
        '    best = min(range(HORIZON - 1), key=lambda i: (rows[i]["headroom_cents"], i))',
    ),
    "r3-04-required-is-capped-peak-plus-shortfall": (
        "Required commitment is the capped peak plus the largest shortfall, a shortcut that is not the free-path peak.",
        '    required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in uncapped])',
        '    required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in rows]) + max(0, case["minimum_cash_cents"] - min(row["ending_cash_cents"] for row in rows))',
    ),
    "r3-05-shortfall-read-off-free-path": (
        "Shortfall is read from the uncapped path, where cash always lands on minimum, so a binding commitment is hidden.",
        '    shortfall = max([0] + [max(0, minimum - row["ending_cash_cents"]) for row in rows])',
        '    shortfall = max([0] + [max(0, minimum - row["ending_cash_cents"]) for row in uncapped])',
    ),
}

for name, (desc, old, new) in EDITS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1)
    header = f'"""Mutant {name}: {desc}"""\n'
    rest = text.split('"""', 2)[2].lstrip("\n")
    (OUT / f"{name}.py").write_text(header + "\n" + rest, encoding="utf-8")
    print("wrote", name)
