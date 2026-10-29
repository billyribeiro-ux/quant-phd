"""Write the round-25 student-error mutants of the CF1 reference engine into ledgers/CF1/mutants/ (each edit must match once)."""
import pathlib
ROOT = pathlib.Path("/tmp/verify25-CF1-d")
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
MUTANTS = {
    "v25d_01_payback_ignores_discount_rate.py": (
        "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n",
        "    discounted = [cf for cf in flows]\n",
        "v25d_01: payback with rate > 0 ignores the rate and returns the simple (undiscounted) payback, although the page says each flow is first divided by (1 + rate) ** t.",
    ),
    "v25d_02_fisher_adds_the_two_rates.py": (
        "    return (1.0 + real) * (1.0 + inflation) - 1.0\n",
        "    return real + inflation\n",
        "v25d_02: the Fisher conversion adds the two rates, the rule of thumb that the page says is not the identity (1 + nominal) = (1 + real) x (1 + inflation).",
    ),
    "v25d_03_monte_carlo_no_mean_one_correction.py": (
        "        m = math.exp(volatility * z - volatility * volatility / 2.0)\n",
        "        m = math.exp(volatility * z)\n",
        "v25d_03: the Monte Carlo multiplier omits the - volatility**2 / 2 term, so E[m] is not one and the mean NPV drifts from the deterministic NPV.",
    ),
    "v25d_04_negative_tax_floored_at_zero.py": (
        "        tax = tax_rate * (ebitda - depreciation)\n",
        "        tax = max(0.0, tax_rate * (ebitda - depreciation))\n",
        "v25d_04: a negative tax is floored at zero, so a loss gives no credit, although the page says a negative tax is a credit.",
    ),
}
for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new)
    body = f'"""{desc}\n\nMutant of the reference solution for the CF1 capital-budgeting engine (capbudget.py).\n"""\n'
    out = ROOT / "ledgers/CF1/mutants" / name
    out.write_text(body + text.split('"""', 2)[2], encoding="utf-8")
    print("wrote", name)
