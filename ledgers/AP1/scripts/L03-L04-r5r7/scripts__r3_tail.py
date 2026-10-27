"""Round-5: sensitivity of the truth bounds to the tail (ray atom M and the dense range)."""

import sys

sys.path.insert(0, "/tmp/ap1-r5/L03-L04/scripts")
import r3_lp  # noqa: E402
from r3_lp import STRIKES, bounds, ge, gt  # noqa: E402

wide = [round(i * 0.05, 10) for i in range(0, 20001)]  # 0..1000
for M in (1.0e4, 1.0e6):
    r3_lp.M_RAY = M
    for k in (95.0, 97.3):
        for name, mk in (("ge", ge), ("gt", gt)):
            print(f"M={M:g} k={k} {name} wide(0..1000 step .05)+k,k+-1e-6:",
                  bounds(wide + [k - 1e-6, k, k + 1e-6], mk(k)),
                  " page recipe d=1e-5:", bounds([0.0] + STRIKES + [k - 1e-5, k, k + 1e-5], mk(k)))
    sys.stdout.flush()
