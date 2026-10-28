"""Build round-13 verifier mutants (ledgers/CF1/mutants) and alternative engines from the reference solution."""
import sys
from pathlib import Path

ROOT = Path("/tmp/verify13-CF1-d")
REF = ROOT / "course/modules/CF/CF1/grader/reference.py"
MUT = ROOT / "ledgers/CF1/mutants"
ALT = Path("/tmp/verify13-CF1-d/ledgers/CF1/scripts/CF1-d-r13/alts")
ALT.mkdir(parents=True, exist_ok=True)


def make(src: str, edits: list[tuple[str, str]], doc: str) -> str:
    out = src
    for old, new in edits:
        assert out.count(old) == 1, ("edit not unique or missing", old[:60])
        out = out.replace(old, new)
    # replace the reference module docstring with the mutant description
    head, sep, rest = out.partition('"""')
    _, sep2, tail = rest.partition('"""')
    assert sep and sep2
    return f'"""{doc}"""' + tail


ref = REF.read_text(encoding="utf-8")

muts = {
    "r13v_01_monte_carlo_new_generator_each_draw.py": (
        [("    rng = random.Random(seed)\n    out: list[float] = []\n    for _ in range(n_draws):\n        z = rng.gauss(0.0, 1.0)",
          "    out: list[float] = []\n    for _ in range(n_draws):\n        z = random.Random(seed).gauss(0.0, 1.0)")],
        "The student builds a new random.Random(seed) inside the loop, so every draw takes the same first normal number instead of the next one of the single seeded stream.",
    ),
    "r13v_02_irr_grid_linear_in_discount_factor.py": (
        [("    xs = [\n        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))\n        for k in range(_GRID_POINTS)\n    ]",
          "    xs = [_X_LOW + (_X_HIGH - _X_LOW) * k / (_GRID_POINTS - 1) for k in range(_GRID_POINTS)]")],
        "The student spaces the IRR search grid evenly in the discount factor x instead of evenly in log x, so the grid is not the one the page specifies.",
    ),
    "r13v_03_discounted_payback_exponent_one_short.py": (
        [("    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]",
          "    discounted = [cf / (1.0 + rate) ** max(t - 1, 0) for t, cf in enumerate(flows)]")],
        "The student discounts each flow by one year too few (t - 1 instead of t), so the discounted payback is computed with the wrong timing of every flow after the outlay.",
    ),
    "r13v_04_fisher_rounded_to_nine_decimals.py": (
        [("    return (1.0 + real) * (1.0 + inflation) - 1.0",
          "    return round((1.0 + real) * (1.0 + inflation) - 1.0, 9)")],
        "The student rounds the Fisher nominal rate to nine decimal places, so the exact identity (1 + nominal) = (1 + real)(1 + inflation) holds only to about 1e-9, not to the stated relative 1e-12.",
    ),
}

alts = {
    "alt_r13v_a_life_whole_float_accepted.py": (
        [("    if not isinstance(life, int) or isinstance(life, bool) or life < 1:",
          "    if isinstance(life, bool) or not _finite(life) or float(life) != int(life) or life < 1:")],
        "Alternative: a life given as a whole-number float (2.0) is accepted, as the spec's 'whole number' allows.",
    ),
    "alt_r13v_b_fisher_via_log1p_expm1.py": (
        [("    return (1.0 + real) * (1.0 + inflation) - 1.0",
          "    return math.expm1(math.log1p(real) + math.log1p(inflation))")],
        "Alternative: the Fisher nominal rate computed as expm1(log1p(real) + log1p(inflation)), the same exact identity by another route.",
    ),
    "alt_r13v_c_npv_horner_from_last_flow.py": (
        [("    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
          "    v = 1.0 / (1.0 + rate)\n    acc = 0.0\n    for cf in reversed(flows):\n        acc = acc * v + cf\n    return acc")],
        "Alternative: NPV by Horner's rule on the flows (a different valid arithmetic route to the same sum).",
    ),
}

for name, (edits, doc) in muts.items():
    (MUT / name).write_text(make(ref, edits, doc), encoding="utf-8")
    print("wrote mutant", name)

ALT.mkdir(parents=True, exist_ok=True)
for name, (edits, doc) in alts.items():
    (ALT / name).write_text(make(ref, edits, doc), encoding="utf-8")
    print("wrote alt", name)
