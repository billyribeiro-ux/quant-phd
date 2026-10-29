"""For seeds in a range, the largest entry gap between the reference projection and clipping on the seeded corr.

Usage: clip_vs_projection_gap.py <first_seed> <last_seed>. Prints the seeds whose gap is at most 1e-3, which is the
case where test_projection_repair_differs_from_clipping_on_this_instance would fail a correct projection.
"""

from __future__ import annotations

import sys
from pathlib import Path

CHECKOUT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(CHECKOUT / "course" / "modules" / "M" / "M3" / "grader"))

import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402


def main() -> int:
    first, last = int(sys.argv[1]), int(sys.argv[2])
    small: list[tuple[int, float]] = []
    gaps: list[float] = []
    for seed in range(first, last + 1):
        for s in (seed, seed + 7_919):  # the two instances the suite uses for a seed
            corr = make_instance(s)["corr"]
            proj = ref.projection_repair(corr)
            clip = ref.clip_repair(corr)
            gap = max(abs(proj[i][j] - clip[i][j]) for i in range(len(corr)) for j in range(len(corr)))
            gaps.append(gap)
            if gap <= 1e-3:
                small.append((s, gap))
    print(f"instances {len(gaps)}, min gap {min(gaps):.3e}, max gap {max(gaps):.3e}")
    print(f"instances with gap <= 1e-3: {len(small)} {small[:10]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
