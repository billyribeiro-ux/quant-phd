"""Cross-check the Lab 3 projection numbers with each alternative module's projection_repair (different stop rules).

Run with: .venv/bin/python -I ledgers/M3/scripts/M3-d-r1/lab3_alt_cross_check.py
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

CHECKOUT = Path(__file__).resolve().parents[4]
ALT_DIR = CHECKOUT / "ledgers" / "M3" / "alternatives"
LAB3 = [[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]]
VOLS = [0.10, 0.20, 0.15, 0.30]


def load(path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod


def frob(a, b) -> float:  # type: ignore[no-untyped-def]
    return math.sqrt(sum((a[i][j] - b[i][j]) ** 2 for i in range(4) for j in range(4)))


def main() -> None:
    for path in sorted(ALT_DIR.glob("*.py")) + [CHECKOUT / "course/modules/M/M3/grader/reference.py"]:
        m = load(path)
        proj = m.projection_repair(LAB3)
        clip = m.clip_repair(LAB3)
        w_p = m.comparison_weights(proj, VOLS)
        w_c = m.comparison_weights(clip, VOLS)
        dc, dp = frob(clip, LAB3), frob(proj, LAB3)
        print(
            path.name,
            f"dc={dc:.6f} dp={dp:.6f} gap={dc - dp:.6f}",
            "wc=" + " ".join(f"{x:.6f}" for x in w_c),
            "wp=" + " ".join(f"{x:.6f}" for x in w_p),
            f"maxw={max(abs(a - b) for a, b in zip(w_p, w_c, strict=True)):.6f}",
        )


if __name__ == "__main__":
    main()
