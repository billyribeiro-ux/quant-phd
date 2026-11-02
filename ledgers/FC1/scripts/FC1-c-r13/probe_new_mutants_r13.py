"""Round-13 probe: a valid input the page allows (no upper limit is named) where each new mutant differs from the reference."""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])


def load(path: pathlib.Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load(ROOT / "course/modules/FC/FC1/grader/reference.py", "refm")
m1 = load(ROOT / "ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py", "m1")
m2 = load(ROOT / "ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py", "m2")
m3 = load(ROOT / "ledgers/FC1/mutants/r13n03_yield_rate_through_float.py", "m3")
a = ref.Bond(10**17 + 4999, 1, 1).events()
b = m1.Bond(10**17 + 4999, 1, 1).events()
print("r13n01 coupon: reference", a, "mutant", b, "differs" if a != b else "same")
a = ref.CashTrade(2**40 + 1, 9851, 1, 2).events()
b = m2.CashTrade(2**40 + 1, 9851, 1, 2).events()
print("r13n02 trade: reference", a, "mutant", b, "differs" if a != b else "same")
a = ref.bond_price_cents(ref.Bond(1704285, 179, 1), 496)
b = m3.bond_price_cents(m3.Bond(1704285, 179, 1), 496)
print("r13n03 yield via float: reference", a, "mutant", b, "differs" if a != b else "same")
