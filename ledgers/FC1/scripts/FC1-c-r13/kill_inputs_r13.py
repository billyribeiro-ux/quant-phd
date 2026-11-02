"""Round-13: the three distinguishing inputs for the surviving mutants r13n01..r13n03 (reference vs mutant)."""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/FC/FC1/grader/reference.py", "refk")
for label, mut, call in [
    ("r13n01 coupon in float", "r13n01_coupon_computed_in_float.py", lambda m: m.Bond(10**17 + 4999, 1, 1).events()),
    ("r13n02 trade cash in float", "r13n02_trade_cash_flow_in_float.py", lambda m: m.CashTrade(2**40 + 1, 9851, 1, 2).events()),
    ("r13n03 yield via float", "r13n03_yield_rate_through_float.py", lambda m: m.bond_price_cents(m.Bond(13, 0, 1), 400)),
]:
    m = load(ROOT / "ledgers/FC1/mutants" / mut, mut[:6])
    want = call(ref) if "bond_price" not in mut and "yield" not in mut else ref.bond_price_cents(ref.Bond(13, 0, 1), 400)
    got = call(m)
    print(label, "| reference", want, "| mutant", got, "| distinguishes" if want != got else "| same")
