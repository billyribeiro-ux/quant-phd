"""Check the equivalence claim in ledgers/E4/equivalent/README.md: the literal_price_sign variant and the reference
agree exactly on the three outputs on random inputs (and the README's own input ranges).

Usage: python -I ledgers/E4/scripts/E4-d-r2/check_equivalent.py <repo-root>
"""

import importlib.util
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load(root / "course/modules/E/E4/grader/reference.py", "ref")
eq = load(root / "ledgers/E4/equivalent/literal_price_sign.py", "eq")
rng = random.Random(20261103)
worst = 0.0
n = 0
for _ in range(3000):
    sd = rng.uniform(0.05, 3.0)
    c = rng.uniform(0.0, 0.4)
    a = ref.solve_model(sd, c)
    b = eq.solve_model(sd, c)
    for k in a:
        worst = max(worst, abs(a[k] - b[k]))
    n += 1
print("pairs compared:", n, "largest absolute difference over the three outputs:", worst)
print("b_u sign in equivalent variant:", "b_u = +a" in (root / "ledgers/E4/equivalent/literal_price_sign.py").read_text(encoding="utf-8") or "see diff")
