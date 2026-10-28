"""Round-22 student-error mutants of the CF1 reference engine (new this round), written to ledgers/CF1/mutants/."""
import pathlib

CHK = pathlib.Path("/tmp/verify22-CF1-d")
REF = (CHK / "course/modules/CF/CF1/grader/reference.py").read_text()
MUT = CHK / "ledgers/CF1/mutants"


def swap(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)


mutants = {
    "r22d_01_discounted_payback_accumulates_undiscounted_flows.py": (
        "Discounted payback accumulates the undiscounted flows in the cumulative sum, but still divides by the discounted flow.",
        [
            ("        if cumulative + discounted[t] >= 0.0:", "        if cumulative + flows[t] >= 0.0:"),
            ("        cumulative += discounted[t]", "        cumulative += flows[t]"),
        ],
    ),
    "r22d_02_working_capital_uses_same_year_revenue.py": (
        "Working capital at the end of year t is set from the revenue of year t instead of year t - 1.",
        [("        nwc[t] = share * revenue[t - 1]", "        nwc[t] = share * revenue[t]")],
    ),
    "r22d_03_npv_refuses_a_zero_rate.py": (
        "NPV refuses a zero rate, as if the rate had to be strictly positive.",
        [
            (
                "    _check_rate(rate)\n    if len(flows) == 0:",
                '    _check_rate(rate)\n    if rate == 0.0:\n        raise ValueError("rate must be positive")\n    if len(flows) == 0:',
            )
        ],
    ),
    "r22d_04_payback_needs_strictly_positive_cumulative.py": (
        "Payback is the first year in which the cumulative flow is strictly above zero, so an exact recovery is missed.",
        [("        if cumulative + discounted[t] >= 0.0:", "        if cumulative + discounted[t] > 0.0:")],
    ),
}

for name, (doc, reps) in mutants.items():
    src = REF
    for old, new in reps:
        src = swap(src, old, new)
    # Mirror the earlier mutants: one-line description docstring, then the reference body without its module docstring.
    body = src.split('"""', 2)[2]
    (MUT / name).write_text('"""' + doc + '"""' + body)
    print("wrote", name)
