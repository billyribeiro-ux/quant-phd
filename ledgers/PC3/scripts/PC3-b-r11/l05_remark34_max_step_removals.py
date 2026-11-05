"""Maximum number of back removals in one step of the L05 deque (Remark 3.4 'up to k-1' check). Stdlib only."""

from __future__ import annotations

import itertools


def max_removals_one_step(xs: list[int], k: int) -> tuple[int, int]:
    """Return (largest back-removal count in a single step i, the step index that attains it), 1-based i."""
    dq: list[int] = []
    best, best_step = 0, 0
    for i in range(1, len(xs) + 1):
        removed = 0
        while dq and xs[dq[-1] - 1] <= xs[i - 1]:
            dq.pop()
            removed += 1
        if removed > best:
            best, best_step = removed, i
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
    return best, best_step


def main() -> None:
    for k in range(2, 6):
        worst = (0, None, None)
        for n in range(k, 9):
            for xs in itertools.product(range(4), repeat=n):
                r, step = max_removals_one_step(list(xs), k)
                if r > worst[0]:
                    worst = (r, n, xs)
        print(f"k={k}: largest back-removal count in one step over all sequences n<=8 over {{0..3}}: "
              f"{worst[0]} (witness n={worst[1]}, x={worst[2]})")
    print("example x=(2,1,3), k=2: removals at step 3 =", max_removals_one_step([2, 1, 3], 2))


if __name__ == "__main__":
    main()
