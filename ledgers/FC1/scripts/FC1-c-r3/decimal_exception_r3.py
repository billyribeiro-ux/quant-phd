"""Round-3 (verifier D3): the ten-digit Decimal mutant at yield -9999 on the seed-0 bond, and on a 1-period bond. Usage: <root>."""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("instance", root / "course/modules/FC/FC1/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
spec2 = importlib.util.spec_from_file_location("dec", root / "ledgers/FC1/mutants/r3c_price_ten_significant_digits.py")
dec = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(dec)
c = inst.make_instance(0)
bond = dec.Bond(c["face_cents"], c["coupon_bps"], c["periods"])
try:
    print("seed-0 bond at -9999:", dec.bond_price_cents(bond, -9999))
except Exception as e:  # report the type, not the message
    print("seed-0 bond at -9999 raises", type(e).__name__)
print("one-period bond 10000/500/1 at -9999:", dec.bond_price_cents(dec.Bond(10000, 500, 1), -9999))
