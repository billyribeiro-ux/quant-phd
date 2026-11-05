"""PC3-b round 11: independent check of the corrected L05 Remark 3.4 (stdlib only, no lab code imported).

Claims checked (course/modules/PC/PC3/L05.html line 147):
 (a) the witness x=(k,k-1,...,1,k+1), n=k+1, makes step k+1 remove exactly k entries (loop removals and expiry);
     after step k the deque holds indices 1..k in decreasing value.
 (b) before step i the deque holds only indices in {i-k,...,i-1}, so one step removes at most k entries.
 (c) every removal at step i is one of those indices.
 (d) exhaustive search: over all sequences with n<=7 over values {0..k+1} (k=1..4), the largest number of entries
     removed in one step equals k, never k+1 or more.
Run from the checkout root: python -I ledgers/PC3/scripts/PC3-b-r11/l05_remark34_r11.py
"""

from __future__ import annotations

import itertools


def run(xs: list[int], k: int) -> list[tuple[int, list[int], list[int], list[int]]]:
    """Return per step i (1-based): (i, deque before step, indices removed at step i, deque after step i).

    Removed = indices taken from the back by the while loop plus the one front index removed by expiry.
    """
    dq: list[int] = []
    steps = []
    for i in range(1, len(xs) + 1):
        before = list(dq)
        removed: list[int] = []
        while dq and xs[dq[-1] - 1] <= xs[i - 1]:
            removed.append(dq.pop())
        dq.append(i)
        if dq[0] <= i - k:
            removed.append(dq.pop(0))
        steps.append((i, before, removed, list(dq)))
    return steps


def main() -> int:
    ok = True
    # (a) and (b),(c) on the witness family
    for k in range(1, 11):
        xs = list(range(k, 0, -1)) + [k + 1]
        n = k + 1
        assert len(xs) == n
        steps = run(xs, k)
        _, _, removed_k1, _ = steps[k]  # step k+1 (0-based index k)
        after_k = steps[k - 1][3]
        cond_a = len(removed_k1) == k and sorted(removed_k1) == list(range(1, k + 1)) and after_k == list(range(1, k + 1))
        ok &= cond_a
        print(f"(a) k={k:>2} x={xs}: after step k deque={after_k}; step {k + 1} removes {len(removed_k1)} "
              f"indices {sorted(removed_k1)}: {cond_a}")
    # (b),(c) on every sequence of length <= 7 over {0..k+1}, all k <= 4
    for k in range(1, 5):
        worst = 0
        bad = 0
        for n in range(1, 8):
            for xs in itertools.product(range(k + 2), repeat=n):
                for i, before, removed, after in run(list(xs), k):
                    lo = max(1, i - k)
                    if not all(lo <= j <= i - 1 for j in before):
                        bad += 1
                    if not all(lo <= j <= i - 1 for j in removed):
                        bad += 1
                    worst = max(worst, len(removed))
        print(f"(b,c,d) k={k}: sequences over {{0..{k + 1}}} with n<=7: largest entries removed in one step = {worst}; "
              f"violations of (b)/(c) = {bad}")
        ok &= worst == k and bad == 0
    print(f"ALL CHECKS PASS: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
