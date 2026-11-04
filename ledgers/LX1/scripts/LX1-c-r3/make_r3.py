"""Round-3 LX1-c: write NEW student-error mutants (ledgers/LX1/mutants/) and alternative correct implementations
(ledgers/LX1/scripts/LX1-c-r3/gen/) from the lab twins. Each replacement must match exactly once."""
import os
import sys

ROOT = sys.argv[1]
T = os.path.join(ROOT, "tests/labs/LX1")
M = os.path.join(ROOT, "ledgers/LX1/mutants")
G = os.path.join(ROOT, "ledgers/LX1/scripts/LX1-c-r3/gen")


def make(src_lab, dst_dir, name, pairs):
    text = open(os.path.join(T, src_lab + ".py"), encoding="utf-8").read()
    for old, new in pairs:
        n = text.count(old)
        assert n == 1, (name, old, n)
        text = text.replace(old, new)
    open(os.path.join(dst_dir, name), "w", encoding="utf-8").write(text)


MUT = [
    ("lx1c_r3n01_lab2_debt_entered_in_dollars_as_cents.py", "lab-LX1-project-2",
     [("NOMINAL_DEBT_CENTS = 4_000_000", "NOMINAL_DEBT_CENTS = 40_000")]),
    ("lx1c_r3n02_lab3_window_three_starts_one_month_early.py", "lab-LX1-project-3",
     [('WINDOW_THREE_FROM = "2025-10"', 'WINDOW_THREE_FROM = "2025-09"')]),
    ("lx1c_r3n03_lab3_ratio_from_rounded_sds.py", "lab-LX1-project-3",
     [('print(f"ratio of window two to window one sd, two decimals: {show(sd_two / sd_one, 2)}")',
       'print(f"ratio of window two to window one sd, two decimals: {show(float(show(100 * sd_two, 2)) / float(show(100 * sd_one, 2)), 2)}")')]),
    ("lx1c_r3n04_lab3_zero_threshold_1e-3.py", "lab-LX1-project-3",
     [("zeros = sum(1 for value in values if value == 0.0)", "zeros = sum(1 for value in values if abs(value) < 1e-3)")]),
]
ALT = [
    ("alt_lab2_burden_as_end_minus_start.py", "lab-LX1-project-2",
     [("    return 100 * (start_price / end_price - 1)", "    return 100 * (start_price - end_price) / end_price")]),
    ("alt_lab2_real_value_via_fraction_reciprocal.py", "lab-LX1-project-2",
     [("    return ___", "    return Fraction(nominal_cents) * (1 / price_level)")]) if False else
    ("alt_lab2_real_value_via_reciprocal.py", "lab-LX1-project-2",
     [("    return Fraction(nominal_cents) / price_level", "    return Fraction(nominal_cents) * (1 / price_level)")]),
    ("alt_lab3_welford_sd.py", "lab-LX1-project-3",
     [("def sample_sd_two_pass(values: Sequence[float]) -> float:\n",
       "def sample_sd_two_pass(values: Sequence[float]) -> float:\n"
       "    mean_w = 0.0\n    m2 = 0.0\n    for k, x in enumerate(values, 1):\n"
       "        d = x - mean_w\n        mean_w += d / k\n        m2 += d * (x - mean_w)\n"
       "    return math.sqrt(m2 / (len(values) - 1))\n\n\ndef _unused_two_pass(values: Sequence[float]) -> float:\n")]),
    ("alt_lab3_log1p_changes.py", "lab-LX1-project-3",
     [("return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]",
       "return [(month, math.log1p(float((rate - previous) / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]")]),
    ("alt_lab3_stdev_only_no_two_pass.py", "lab-LX1-project-3",
     [("    sd = sample_sd_two_pass(values)\n    if abs(100 * (sd - statistics.stdev(values))) > AGREEMENT:\n        raise ValueError(\"the two-pass and statistics.stdev standard deviations disagree\")\n",
       "    sd = statistics.stdev(values)\n")]),
]
for name, lab, pairs in MUT:
    make(lab, M, name, pairs)
os.makedirs(G, exist_ok=True)
for name, lab, pairs in ALT:
    make(lab, G, name, pairs)
print("wrote", len(MUT), "mutants and", len(ALT), "alternatives")
