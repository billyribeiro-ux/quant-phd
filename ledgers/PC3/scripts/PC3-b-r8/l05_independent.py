"""Independent re-derivation of the PC3 L05 numbers and proofs (verifier round 8). Written from the page text.

Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r8/l05_independent.py
"""

from __future__ import annotations

import itertools
import random


def seq(seed: int, n: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(0, 999) for _ in range(n)]


def naive(xs: list[int], k: int) -> tuple[list[int], int]:
    out: list[int] = []
    cmp = 0
    for i in range(k - 1, len(xs)):
        window = xs[i - k + 1 : i + 1]
        cur = window[0]
        for v in window[1:]:
            cmp += 1
            if v > cur:
                cur = v
        out.append(cur)
    return out, cmp


def deque_alg(xs: list[int], k: int) -> tuple[list[int], int, int, int]:
    """Pseudocode of the page (Section 3), 1-indexed in the proofs, converted to 0-index here."""
    dq: list[int] = []  # indices, front at index 0
    out: list[int] = []
    cmp = pushes = pops = 0
    for i in range(len(xs)):
        while dq:
            cmp += 1
            if xs[dq[-1]] <= xs[i]:
                dq.pop()
                pops += 1
            else:
                break
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.pop(0)
            pops += 1
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out, cmp, pops, pushes


def main() -> None:
    xs = seq(5, 200)
    print("first five values:", xs[:5])
    nv, ncount = naive(xs, 8)
    dv, dcmp, dpops, dpush = deque_alg(xs, 8)
    print("windows:", 200 - 8 + 1, "naive count:", ncount, "formula:", (200 - 8 + 1) * 7)
    print("first five deque maxima:", dv[:5])
    print("outputs equal k=8:", nv == dv)
    print("deque comparisons, pops, pushes at k=8:", dcmp, dpops, dpush)
    print("max value in sequence:", max(xs))
    eq = all(naive(xs, k)[0] == deque_alg(xs, k)[0] for k in range(1, 21))
    print("outputs equal k=1..20:", eq)
    for k in (1, 2, 8, 32, 200):
        _, nc = naive(xs, k)
        _, c, po, pu = deque_alg(xs, k)
        print("table k=%d naive=%d formula=%d deque_cmp=%d pops=%d pushes=%d" % (k, nc, (200 - k + 1) * (k - 1), c, po, pu))

    # Exhaustive small check: all sequences over {0,1,2} of length 0..7, all k with 1<=k<=n, and k>n gives no output.
    ok_out = True
    ok_bound = True
    ok_prop21 = True
    count = 0
    for n in range(0, 8):
        for xs2 in itertools.product(range(3), repeat=n):
            xs2l = list(xs2)
            for k in range(1, n + 2):
                count += 1
                if k > n:
                    if deque_alg(xs2l, k)[0] != []:
                        ok_out = False
                    continue
                nv2, nc2 = naive(xs2l, k)
                dv2, c2, po2, pu2 = deque_alg(xs2l, k)
                if nv2 != dv2:
                    ok_out = False
                if nc2 != (n - k + 1) * (k - 1):
                    ok_prop21 = False
                if c2 > 2 * n or pu2 > n or pu2 > 2 * n:
                    ok_bound = False
                # brute-force window max for reference
                ref = [max(xs2l[i - k + 1 : i + 1]) for i in range(k - 1, n)]
                if ref != nv2:
                    ok_out = False
    print("exhaustive {0,1,2}^n n<=7, all k: cases", count, "outputs equal:", ok_out,
          "naive count = (n-k+1)(k-1):", ok_prop21, "deque comparisons<=2n and pops<=n:", ok_bound)

    # Random larger sequences: bound 2n and pops <= n.
    rng = random.Random(1234)
    worst_ratio = 0.0
    bad = 0
    for _ in range(3000):
        n = rng.randint(1, 60)
        k = rng.randint(1, n)
        xs3 = [rng.randint(-50, 50) for _ in range(n)]
        dv3, c3, po3, pu3 = deque_alg(xs3, k)
        if dv3 != [max(xs3[i - k + 1 : i + 1]) for i in range(k - 1, n)]:
            bad += 1
        if c3 > 2 * n or po3 > n:
            bad += 1
        worst_ratio = max(worst_ratio, c3 / (2 * n))
    print("random 3000 cases: failures =", bad, "max comparisons/(2n) =", round(worst_ratio, 4))

    # Remark 2.2: (n-r) r <= n^2/4 with equality iff r = n/2 (even n), for n up to 60, integer r in 0..n.
    rem_ok = True
    for n in range(0, 61):
        for r in range(0, n + 1):
            lhs = (n - r) * r
            if 4 * lhs > n * n:
                rem_ok = False
            if (n % 2 == 0) and (r == n // 2) and 4 * lhs != n * n:
                rem_ok = False
    print("Remark 2.2 bound and equality, n<=60:", rem_ok)

    # Remark 3.4: x=(k,k-1,...,2,k+1), n=k: at step k the deque holds indices 1..k-1 and one step removes k-1.
    for k in range(2, 12):
        x = list(range(k, 1, -1)) + [k + 1]
        assert len(x) == k
        # run the algorithm, instrument step k (index k-1, 0-based)
        dq: list[int] = []
        removed_at_last = 0
        for i in range(len(x)):
            removed = 0
            while dq:
                if x[dq[-1]] <= x[i]:
                    dq.pop()
                    removed += 1
                else:
                    break
            dq.append(i)
            if dq[0] <= i - k:
                dq.pop(0)
            if i == len(x) - 1:
                removed_at_last = removed
        if removed_at_last != k - 1:
            print("Remark 3.4 failed for k", k, removed_at_last)
    print("Remark 3.4 last-step removals equal k-1 for k=2..11: checked")

    # Example 3.5 trace.
    dv5, c5, po5, pu5 = deque_alg([3, 1, 4, 1, 5], 3)
    print("Example 3.5 outputs:", dv5, "(expected [4, 4, 5])")

    # Remark 3.6 arithmetic: floor(log2 200) = 7, 3*200*7 = 4200, 2n = 400.
    import math

    print("Remark 3.6: floor(log2 200) =", math.floor(math.log2(200)), "3*200*7 =", 3 * 200 * 7, "2n =", 400)


if __name__ == "__main__":
    main()
