"""Load the L02 twin's functions without running main() and print the SIMULATED filer's raw values."""
import importlib.util
import sys

TWIN = "/tmp/verify-ac2r6-l12/tests/labs/AC2/lab-AC2-L02-1.py"
NOEXEC = "/tmp/ac2-v/l12/r6/lab_l02_noexec.py"
src = open(TWIN, encoding="utf-8").read().rstrip()
assert src.endswith("main()")
open(NOEXEC, "w", encoding="utf-8").write(src[: -len("main()")])
spec = importlib.util.spec_from_file_location("lab_l02_noexec", NOEXEC)
m = importlib.util.module_from_spec(spec)
sys.modules["lab_l02_noexec"] = m
spec.loader.exec_module(m)
f = m.make_filer()
st = m.standardize(f)
sa = m.standardize(f, as_of="2023-06-30")
for end in st:
    print(end, {k: st[end].get(k) for k in ("revenue", "cogs", "net_income", "equity", "receivables", "total_assets")})
print("2022 revenue as of 2023-06-30:", sa["2022-12-31"]["revenue"])
print("recv/orig rev*365 =", round(st["2022-12-31"]["receivables"] / sa["2022-12-31"]["revenue"] * 365, 3))
print("recv/restated rev*365 =", round(st["2022-12-31"]["receivables"] / st["2022-12-31"]["revenue"] * 365, 3))
print("equity growth 2021->2022:", round(st["2022-12-31"]["equity"] / st["2021-12-31"]["equity"] - 1, 4))
