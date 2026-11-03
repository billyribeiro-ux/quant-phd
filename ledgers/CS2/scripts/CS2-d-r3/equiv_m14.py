"""Compare the reference sketch with the no-clamp variant (rank_target_without_clamp.py) on every stream of length
0..6 over {0,1,2} (exhaustive, ordering of adds fixed as given) and on random streams, for epsilon in {0.05, 0.1, 0.2, 0.3}
and q in k/40 and the seven-decimal probe 0.2500004 and 0.1. Outputs must be equal or both raise the same exception type.
Usage: python -I equiv_m14.py <reference.py> <variant.py>"""

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load(p: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, Path(p).resolve())
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


A = load(sys.argv[1], "a")
B = load(sys.argv[2], "b")
QS = [k / 40 for k in range(41)] + [0.1, 0.2500004, 0.05]
EPS = [0.05, 0.1, 0.2, 0.3]


def run(mod, stream, eps, q):  # type: ignore[no-untyped-def]
    sk = mod.QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    try:
        return ("ok", sk.quantile(q))
    except Exception as e:  # noqa: BLE001
        return ("err", type(e).__name__)


checked = 0
diff = 0
streams = []
for n in range(0, 7):
    for vals in itertools.product((0.0, 1.0, 2.0), repeat=n):
        streams.append(list(vals))
rng = random.Random(3)
for _ in range(120):
    streams.append([round(rng.uniform(-3, 3), 2) for _ in range(rng.randint(1, 40))])
for s in streams:
    for eps in EPS:
        sa = A.QuantileSketch(eps)
        sb = B.QuantileSketch(eps)
        for x in s:
            sa.add(x)
            sb.add(x)
        for q in QS:
            checked += 1
            ra = sa.quantile(q) if s else None
            rb = sb.quantile(q) if s else None
            try:
                va = ("ok", sa.quantile(q))
            except Exception as e:  # noqa: BLE001
                va = ("err", type(e).__name__)
            try:
                vb = ("ok", sb.quantile(q))
            except Exception as e:  # noqa: BLE001
                vb = ("err", type(e).__name__)
            if va != vb:
                diff += 1
print(f"streams {len(streams)}, (stream, eps, q) checks {checked}, differences {diff}")
