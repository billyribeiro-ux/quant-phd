"""Round 5 FC2-d: write four new student-error mutants of reference.py into ledgers/FC2/mutants/ (one-line docstring first)."""
import pathlib, sys
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d")
REF = (ROOT / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC2/mutants"
def mutate(name, description, pairs):
    src = REF
    for old, new in pairs:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    body = f'"""{description}\n\nNot deployed (BLUEPRINT section 7). Round 5 verifier mutant for FC2-d.\n"""\n'
    src = src.split('"""', 2)[2].lstrip("\n")  # drop reference docstring
    (OUT / name).write_text(body + "\n" + src, encoding="utf-8")
    print("wrote", name)
mutate("r5_a_float_discount_ties.py",
       "Student error: the discounted strike and the gap are computed in floating point, so an exact half-cent tie can round the wrong way.",
       [("from fractions import Fraction\n", "import math\nfrom fractions import Fraction\n"),
        ("    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))\n    return _half_up(gap)",
         "    gap = call_cents - put_cents - (spot_cents - strike_cents * (df_ppm / PPM))\n    return math.floor(gap + 0.5)"),
        ("        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))\n        gross = _half_up(abs(gap))",
         "        gap = calls[k] - puts[k] - (spot - strike * (df_ppm / PPM))\n        gross = math.floor(abs(gap) + 0.5)"),
        ("_explain_parity(_half_up(gap), net, fee, spread)", "_explain_parity(math.floor(gap + 0.5), net, fee, spread)")])
mutate("r5_b_swapped_chord_weights.py",
       "Student error: the chord weights are swapped, so each neighbour is weighted by the distance to the wrong end of the grid.",
       [("    w_low = Fraction(high - mid, high - low)\n    w_high = Fraction(mid - low, high - low)\n    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]",
         "    w_low = Fraction(mid - low, high - low)\n    w_high = Fraction(high - mid, high - low)\n    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]")])
mutate("r5_c_parity_loop_skips_first_strike.py",
       "Student error: the parity loop starts at the second strike, so a parity finding at the lowest strike is never reported.",
       [("    for k, strike in enumerate(strikes):\n        gap = Fraction(calls[k])",
         "    for k, strike in enumerate(strikes[1:], start=1):\n        gap = Fraction(calls[k])")])
mutate("r5_d_explanation_direction_reversed.py",
       "Student error: the parity explanation states the trade for the wrong sign of the gap (the call rich case is described as cheap).",
       [('        action = "sell the call, buy the put and the underlying, and borrow the discounted strike"\n        direction = "the call less the put exceeds the spot less the discounted strike"',
         '        action = "buy the call, sell the put and the underlying, and lend the discounted strike"\n        direction = "the call less the put exceeds the spot less the discounted strike"')])
