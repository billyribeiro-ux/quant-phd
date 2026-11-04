"""Write this round's lab-2 student-error mutants (ledgers/LX2/mutants) and alternative correct implementations (scripts/LX2-c-r5/alts) from the twin, asserting each replacement applies exactly once."""
import os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE5-LX2-c"
TWIN = os.path.join(ROOT, "tests/labs/LX2/lab-LX2-project-2.py")
src = open(TWIN, encoding="utf-8").read()
HIT = "    hit_rate = Fraction(hits, horizon)\n"
BIAS = "    bias = Fraction(sum(errors), horizon)\n"
assert src.count(HIT) == 1 and src.count(BIAS) == 1

def variant(hit_line, bias_line):
    assert hit_line != HIT or bias_line != BIAS
    out = src
    if hit_line != HIT:
        out = out.replace(HIT, hit_line, 1)
    if bias_line != BIAS:
        out = out.replace(BIAS, bias_line, 1)
    return out

mutants = {
    "r5_lab2_bias_divides_by_hits.py": ("Bias divides the error sum by the hit count (4) instead of H = 6.", HIT, "    bias = Fraction(sum(errors), hits)\n"),
    "r5_lab2_bias_over_H_minus_1.py": ("Bias divides by H - 1 = 5, an off-by-one horizon.", HIT, "    bias = Fraction(sum(errors), horizon - 1)\n"),
    "r5_lab2_hit_rate_counts_misses.py": ("Hit rate counts the misses (horizon minus hits) instead of the hits.", "    hit_rate = Fraction(horizon - hits, horizon)\n", BIAS),
    "r5_lab2_bias_sum_of_forecasts.py": ("Bias uses the sum of the forecasts over the window instead of the sum of the errors.", HIT, "    bias = Fraction(sum(forecast(START_MONTH + i) for i in range(horizon)), horizon)\n"),
    "r5_lab2_hit_rate_is_count.py": ("Hit rate prints the hit count itself, not the share of hits.", "    hit_rate = Fraction(hits, 1)\n", BIAS),
}
alts = {
    "alt-r5-a1-len-of-errors.py": ("ALTERNATIVE (must pass): horizon taken as len(errors) in both measures.", "    hit_rate = Fraction(hits, len(errors))\n", "    bias = Fraction(sum(errors), len(errors))\n"),
    "alt-r5-a2-count-by-generator.py": ("ALTERNATIVE (must pass): hit count recomputed by a generator over the errors, horizon from len(REALISED).", "    hit_rate = Fraction(sum(1 for e in errors if abs(e) <= HIT_BAND), len(REALISED))\n", "    bias = Fraction(sum(errors), len(REALISED))\n"),
    "alt-r5-a3-fraction-arithmetic.py": ("ALTERNATIVE (must pass): Fraction arithmetic in the order (count / 1) / H.", "    hit_rate = Fraction(hits) / horizon\n", "    bias = Fraction(sum(errors), 1) / horizon\n"),
    "alt-r5-a4-float-with-fraction-decimal.py": ("ALTERNATIVE (must pass): float quotients for both measures, printed by the page's decimal_text.", "    hit_rate = hits / horizon\n", "    bias = sum(errors) / horizon\n"),
}
for name, (desc, h, b) in mutants.items():
    text = variant(h, b)
    text = text.replace('"""LX2 project lab 2', f'"""MUTANT (student error): {desc}\n\nLX2 project lab 2', 1)
    open(os.path.join(ROOT, "ledgers/LX2/mutants", name), "w", encoding="utf-8").write(text)
    print("wrote mutant", name)
for name, (desc, h, b) in alts.items():
    text = variant(h, b)
    text = text.replace('"""LX2 project lab 2', f'"""{desc}\n\nLX2 project lab 2', 1)
    open(os.path.join(ROOT, "ledgers/LX2/scripts/LX2-c-r5/alts", name), "w", encoding="utf-8").write(text)
    print("wrote alt", name)
