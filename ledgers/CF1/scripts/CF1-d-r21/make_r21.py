"""Build the round-21 student-error mutants and correct alternatives from the reference engine (new this round)."""
import pathlib, sys
REF = pathlib.Path("/tmp/verify21-CF1-d/course/modules/CF/CF1/grader/reference.py").read_text()
MUT = pathlib.Path("/tmp/verify21-CF1-d/ledgers/CF1/mutants")
ALT = pathlib.Path("/tmp/verify21-CF1-d/ledgers/CF1/scripts/CF1-d-r21/alts")
ALT.mkdir(parents=True, exist_ok=True)

def swap(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)

mutants = {
 "r21d_01_tax_on_ebitda_without_depreciation_shield.py": (
   "Tax is charged on EBITDA without deducting depreciation, so the depreciation tax shield is forgotten.",
   [("tax = tax_rate * (ebitda - depreciation)", "tax = tax_rate * ebitda")]),
 "r21d_02_last_year_working_capital_not_recovered.py": (
   "The working-capital flow in the final year is set to zero, so the recovery of the balance at the end of the life is forgotten.",
   [("        working_capital = -(nwc[t] - nwc[t - 1])\n",
     "        working_capital = -(nwc[t] - nwc[t - 1]) if t < life else 0.0\n")]),
 "r21d_03_monte_carlo_reseeds_inside_the_draw_loop.py": (
   "The generator is created inside the draw loop, so every draw uses the first standard normal of the seed.",
   [("    rng = random.Random(seed)\n    out: list[float] = []\n    for _ in range(n_draws):\n        z = rng.gauss(0.0, 1.0)\n",
     "    out: list[float] = []\n    for _ in range(n_draws):\n        z = random.Random(seed).gauss(0.0, 1.0)\n")]),
 "r21d_04_npv_exponent_starts_at_one.py": (
   "The NPV discounts the flow at period t by (1 + rate) to the power t + 1, so the outlay is discounted by one period.",
   [("return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
     "return sum(cf / (1.0 + rate) ** (t + 1) for t, cf in enumerate(flows))")]),
}
for name, (doc, reps) in mutants.items():
    src = REF
    for old, new in reps:
        src = swap(src, old, new)
    body = src.replace('"""', '"""', 1)
    (MUT / name).write_text('"""' + doc + '"""\n' + src.split('"""', 2)[2] if False else '"""' + doc + '"""\n' + src)
    print("wrote", name)

alts = {
 "alt_r21d_a_monte_carlo_exponent_written_as_half_square.py": [
   ("m = math.exp(volatility * z - volatility * volatility / 2.0)",
    "m = math.exp(volatility * z - 0.5 * volatility**2)")],
 "alt_r21d_b_npv_by_running_discount_factor.py": [
   ("return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
    "df = 1.0\n    total = 0.0\n    for cf in flows:\n        total += cf * df\n        df /= (1.0 + rate)\n    return total")],
 "alt_r21d_c_payback_with_running_discount_factor_and_cumulative.py": [
   ("return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
    "return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))")],
}
for name, reps in alts.items():
    src = REF
    for old, new in reps:
        src = swap(src, old, new)
    (ALT / name).write_text(src)
    print("wrote alt", name)
