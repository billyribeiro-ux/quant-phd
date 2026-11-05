"""Round-10 verifier: an alternative CORRECT completion of project lab 2 (page rung 2): float arithmetic for the real
value and the burden written as 100 * (start - end) / end (algebraically equal to 100 * (start / end - 1)).
Argument 1 is the checkout root. Writes the alternative to argument 2."""
import pathlib, sys
root = pathlib.Path(sys.argv[1])
src = (root / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
a = "    return Fraction(nominal_cents) / price_level"
b = "    return 100 * (start_price / end_price - 1)"
assert src.count(a) == 1 and src.count(b) == 1
src = src.replace(a, "    return nominal_cents / price_level").replace(b, "    return 100 * (start_price - end_price) / end_price")
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8")
print("wrote", sys.argv[2])
