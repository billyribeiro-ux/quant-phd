"""Import the L04 twin without running main(); check exact_rate's refusal and the uneven-pool demonstration."""

import importlib.util
import sys

spec = importlib.util.spec_from_file_location("twin_l04", sys.argv[1])
assert spec is not None and spec.loader is not None
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()\n", "\n")
module = type(sys)("twin_l04")
sys.modules["twin_l04"] = module
exec(compile(src, sys.argv[1], "exec"), module.__dict__)
try:
    module.exact_rate(10_000_001, 10_000, "pool")
    print("10,000,001 over 10,000: no raise")
except ValueError as e:
    print("10,000,001 over 10,000: ValueError:", e)
print("100,000 over 3:", end=" ")
try:
    module.exact_rate(100_000, 3, "demonstration rate")
    print("accepted")
except ValueError:
    print("refused")
print("100,000 over 4:", module.exact_rate(100_000, 4, "d"))
