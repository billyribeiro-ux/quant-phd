"""Round-5: page recipe {k-d, k, k+d} vs variants, against a truth grid that is dense (0.01) plus k, k+-1e-6."""

import sys

sys.path.insert(0, "/tmp/ap1-r5/L03-L04/scripts")
from r3_lp import STRIKES, bounds, ge, gt  # noqa: E402

dense = [round(i * 0.01, 10) for i in range(0, 20001)]
base = [0.0] + STRIKES
for k in (95.0, 100.0, 97.3):
    for name, mk in (("ge", ge), ("gt", gt)):
        g = mk(k)
        truth = bounds(dense + [k - 1e-6, k, k + 1e-6], g)
        print(f"k={k} 1{{S {'>=' if name == 'ge' else '>'} k}} TRUTH {truth}")
        for d in (1.0, 0.1, 0.01, 0.001, 1e-4, 1e-5):
            print(f"   d={d:<7} page {{k-d,k,k+d}} {bounds(base + [k - d, k, k + d], g)}"
                  f" | {{k-d,k+d}} {bounds(base + [k - d, k + d], g)}"
                  f" | {{k}} {bounds(base + [k], g)}"
                  f" | {{k-d}} {bounds(base + [k - d], g)}"
                  f" | {{k+d}} {bounds(base + [k + d], g)}"
                  f" | {{k-d,k}} {bounds(base + [k - d, k], g)}"
                  f" | {{k,k+d}} {bounds(base + [k, k + d], g)}")
    sys.stdout.flush()
