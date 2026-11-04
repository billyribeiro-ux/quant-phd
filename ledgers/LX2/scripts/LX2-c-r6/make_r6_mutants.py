"""Write the round-6 rung-2 student-error mutants (ledgers/LX2/mutants/r6_lab2_*.py) and the alternative correct
implementations (ledgers/LX2/scripts/LX2-c-r6/alts/alt_r6_*.py) from the completed twin, each change applied by an
exact single-occurrence string replacement. Every mutant's docstring first line describes the error.

Usage: python3 -I make_r6_mutants.py <repo_root>
"""
import os
import sys

root = sys.argv[1]
twin = open(os.path.join(root, "tests/labs/LX2/lab-LX2-project-2.py"), encoding="utf-8").read()
FIRST = twin.split("\n", 1)[0]
assert FIRST.startswith('"""LX2 project lab 2'), FIRST
BODY = twin.split("\n", 1)[1]

MUTANTS = {
    "r6_lab2_bias_floor_division.py": (
        "Student error: bias uses floor division, so the bias prints as a whole number of units.",
        [("bias = Fraction(sum(errors), horizon)", "bias = Fraction(sum(errors) // horizon)")],
    ),
    "r6_lab2_hit_rate_rounded_before_print.py": (
        "Student error: the hit rate is rounded to two places before the four-place print (double rounding).",
        [("hit_rate = Fraction(hits, horizon)", "hit_rate = Fraction(round(hits / horizon, 2))")],
    ),
    "r6_lab2_error_printed_as_absolute.py": (
        "Student error: the error is stored as an absolute value, so the signed errors and the bias lose their sign.",
        [("error = predicted - realised", "error = abs(predicted - realised)")],
    ),
    "r6_lab2_edge_months_outside_band.py": (
        "Student error: Part D lists the months outside the band (|error| > 2) instead of those on its edge.",
        [("if abs(e) == HIT_BAND]", "if abs(e) > HIT_BAND]")],
    ),
    "r6_lab2_horizon_is_calibration_length.py": (
        "Student error: H is taken as the twelve calibration months rather than the six months of this window.",
        [("horizon = len(REALISED)", "horizon = 12")],
    ),
    "r6_lab2_forecast_index_off_by_one.py": (
        "Student error: the forecast formula uses t - 1 for the month index, an off-by-one in the case model.",
        [("    return 100 + 2 * t\n", "    return 100 + 2 * (t - 1)\n")],
    ),
    "r6_lab2_bias_drops_last_month.py": (
        "Student error: the bias sums the first five errors only and still divides by the six months of the window.",
        [("bias = Fraction(sum(errors), horizon)", "bias = Fraction(sum(errors[:-1]), horizon)")],
    ),
}

os.makedirs(os.path.join(root, "ledgers/LX2/mutants"), exist_ok=True)
for name, (doc, reps) in MUTANTS.items():
    body = BODY
    for old, new in reps:
        n = body.count(old)
        assert n == 1, (name, old, n)
        body = body.replace(old, new)
    src = f'"""{doc}\n' + body
    open(os.path.join(root, "ledgers/LX2/mutants", name), "w", encoding="utf-8").write(src)
    print("wrote", name)

ALT_DIR = os.path.join(root, "ledgers/LX2/scripts/LX2-c-r6/alts")
os.makedirs(ALT_DIR, exist_ok=True)
ALTS = {
    # 1: integer basis points with an explicit half-up integer rule, then the same printed text
    "alt_r6_a1_integer_basis_points.py": (
        "Alternative correct: integer arithmetic on basis points with an explicit half-up integer rule.",
        [
                        ("    print(f\"Part B: hits {hits} of {horizon}; hit rate {decimal_text(hit_rate, 4)}\")",
             "    hit_bp = (hits * 10000 * 2 + horizon) // (2 * horizon)\n"
             "    print(f\"Part B: hits {hits} of {horizon}; hit rate {hit_bp // 10000}.{hit_bp % 10000:04d}\")"),
            ("    print(f\"Part C: bias {decimal_text(bias, 4)} units per month\")",
             "    s = sum(errors)\n"
             "    mag = (abs(s) * 10000 * 2 + horizon) // (2 * horizon)\n"
             "    sign = '-' if s < 0 and mag != 0 else ''\n"
             "    print(f\"Part C: bias {sign}{mag // 10000}.{mag % 10000:04d} units per month\")"),
        ],
    ),
    "alt_r6_a3_generator_streaming.py": (
        "Alternative correct: a streaming generator of (error, hit) pairs, consumed once for both measures.",
        [
            ("    hit_rate = Fraction(hits, horizon)", "    pairs = list(((forecast(t) - r, is_hit(forecast(t), r)) for t, r in zip(range(START_MONTH, START_MONTH + len(REALISED)), REALISED)))\n"
                                     "    hit_rate = Fraction(sum(1 for _, h in pairs if h), horizon)"),
            ("    bias = Fraction(sum(errors), horizon)", "    bias = Fraction(sum(e for e, _ in pairs), horizon)"),
        ],
    ),
    "alt_r6_a4_fraction_sum.py": (
        "Alternative correct: each error wrapped in Fraction before the sum, then divided by the window length.",
        [
            ("    hit_rate = Fraction(hits, horizon)", "    hit_rate = Fraction(hits, 1) / horizon"),
            ("    bias = Fraction(sum(errors), horizon)", "    bias = sum((Fraction(e, 1) for e in errors), Fraction(0)) / horizon"),
        ],
    ),
    "alt_r6_a5_class_based.py": (
        "Alternative correct: the window held in a small class that computes both measures.",
        [
            ("    hit_rate = Fraction(hits, horizon)", "    win = Window(list(REALISED), START_MONTH)\n    hit_rate = win.hit_rate()"),
            ("    bias = Fraction(sum(errors), horizon)", "    bias = win.bias()"),
            ("def main() -> None:",
             "class Window:\n"
             "    def __init__(self, realised: list[int], start: int) -> None:\n"
             "        self.realised = realised\n"
             "        self.start = start\n"
             "    def errors(self) -> list[int]:\n"
             "        return [forecast(self.start + i) - r for i, r in enumerate(self.realised)]\n"
             "    def hit_rate(self) -> Fraction:\n"
             "        return Fraction(sum(1 for e in self.errors() if abs(e) <= HIT_BAND), len(self.realised))\n"
             "    def bias(self) -> Fraction:\n"
             "        return Fraction(sum(self.errors()), len(self.realised))\n\n\n"
             "def main() -> None:"),
        ],
    ),
}
for name, (doc, reps) in ALTS.items():
    body = BODY
    for old, new in reps:
        n = body.count(old)
        assert n == 1, (name, old[:60], n)
        body = body.replace(old, new)
    src = f'"""{doc}\n' + body
    open(os.path.join(ALT_DIR, name), "w", encoding="utf-8").write(src)
    print("wrote alt", name)

# Round 6, rounding-rule mutants (the format-based one was first written as an alternative; it rounds exact binary ties to even)
FORMAT_MUTANT = {
    "r6_lab2_float_format_ties_even.py": (
        "Student error: quotients printed with format(x, '.4f'), which rounds exact binary ties to even (1/32 prints 0.0312).",
        [("    hit_rate = Fraction(hits, horizon)", "    hit_rate = hits / horizon"),
         ("    bias = Fraction(sum(errors), horizon)", "    bias = sum(errors) / horizon"),
         ("decimal_text(hit_rate, 4)", "format(hit_rate, '.4f')"),
         ("decimal_text(bias, 4)", "format(bias, '.4f')")],
    ),
}
for name, (doc, reps) in FORMAT_MUTANT.items():
    body = BODY
    for old, new in reps:
        assert body.count(old) == 1, (name, old[:60], body.count(old))
        body = body.replace(old, new)
    open(os.path.join(root, "ledgers/LX2/mutants", name), "w", encoding="utf-8").write(f'"""{doc}\n' + body)
    print("wrote format mutant", name)

# Round 6, rounding-rule mutants that the rung-2 data cannot tell apart from the stated rule (see the FAIL row).
ROUNDING = {
    "r6_lab2_round_half_even_ties.py": (
        "Student error: decimal_text rounds ties to even (Python round) where the page states half up.",
        [("    magnitude = math.floor(abs(value) * scale + Fraction(1, 2))",
          "    magnitude = round(abs(value) * scale)")],
    ),
    "r6_lab2_round_half_toward_plus_infinity.py": (
        "Student error: decimal_text rounds halves toward plus infinity, so a negative tie rounds toward zero.",
        [("    magnitude = math.floor(abs(value) * scale + Fraction(1, 2))\n    sign = \"-\" if value < 0 and magnitude != 0 else \"\"",
          "    magnitude = math.floor(value * scale + Fraction(1, 2))\n    sign = \"-\" if magnitude < 0 else \"\"\n    magnitude = abs(magnitude)")],
    ),
}
for name, (doc, reps) in ROUNDING.items():
    body = BODY
    for old, new in reps:
        n = body.count(old)
        assert n == 1, (name, old[:60], n)
        body = body.replace(old, new)
    src = f'"""{doc}\n' + body
    open(os.path.join(root, "ledgers/LX2/mutants", name), "w", encoding="utf-8").write(src)
    print("wrote rounding mutant", name)

# Round 6, a hard-coded answer: the two blanks typed as the printed values (rung 2 check is output-only).
HARD = {
    "r6_lab2_hard_coded_printed_values.py": (
        "Student error: the two blanks are typed as the printed values (0.6667 and 0.1667) instead of the expressions.",
        [("    hit_rate = Fraction(hits, horizon)", "    hit_rate = 0.6667"),
         ("    bias = Fraction(sum(errors), horizon)", "    bias = 0.1667")],
    ),
}
for name, (doc, reps) in HARD.items():
    body = BODY
    for old, new in reps:
        n = body.count(old)
        assert n == 1, (name, old[:60], n)
        body = body.replace(old, new)
    src = f'"""{doc}\n' + body
    open(os.path.join(root, "ledgers/LX2/mutants", name), "w", encoding="utf-8").write(src)
    print("wrote hard-coded mutant", name)
