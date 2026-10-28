"""Write three student-error mutants of the CF1 reference into ledgers/CF1/mutants (round 15, verifier e-set)."""

import pathlib

REF = pathlib.Path("/tmp/verify15-CF1-d/course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/verify15-CF1-d/ledgers/CF1/mutants")

MUTANTS = [
    (
        "r15e_01_fisher_real_rate_of_minus_one_accepted",
        "A student guards the real rate with a strict test, so a real rate of exactly -1 is accepted and gives a nominal rate of -1.",
        "    _check_rate(real)\n    _check_rate(inflation)\n",
        "    if not _finite(real) or real < -1.0:\n"
        "        raise ValueError('real rate must be above -1')\n"
        "    _check_rate(inflation)\n",
    ),
    (
        "r15e_02_monte_carlo_returns_draws_sorted",
        "A student sorts the Monte Carlo NPVs for the quantiles and returns them sorted, not in draw order.",
        "    return out\n",
        "    return sorted(out)\n",
    ),
    (
        "r15e_03_payback_fraction_from_discounted_cumulative_undiscounted",
        "A student accumulates the undiscounted flows for the recovery test but takes the fraction from the discounted flow.",
        "        if cumulative + discounted[t] >= 0.0:\n"
        "            return (t - 1) + (-cumulative) / discounted[t]\n"
        "        cumulative += discounted[t]\n",
        "        if cumulative + flows[t] >= 0.0:\n"
        "            return (t - 1) + (-cumulative) / discounted[t]\n"
        "        cumulative += flows[t]\n",
    ),
]

for name, doc, old, new in MUTANTS:
    assert REF.count(old) == 1, name
    body = REF.replace(old, new)
    body = f'"""{doc}"""\n\n' + body[body.index("from __future__") :]
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
