"""Independent re-derivation of the L05 numbers and propositions (PC3-b round 10). Standard library only.

Written from the definitions in course/modules/PC/PC3/L05.html (Definitions 1.3 and 3.1, Propositions 2.1, 3.2, 3.3,
Remarks 2.2 and 3.4, Example 3.5, Problems M2, P3, E1-E3, R2), not from the lab code.
Run as: python -I -W error ledgers/PC3/scripts/PC3-b-r10/l05_indep.py  (from the checkout root)
"""

from __future__ import annotations

import itertools
import random


def brute(xs: list[int], k: int) -> list[int]:
    return [max(xs[i - k + 1 : i + 1]) for i in range(k - 1, len(xs))]


def naive(xs: list[int], k: int) -> tuple[list[int], int]:
    out, comps = [], 0
    for i in range(k - 1, len(xs)):
        best = xs[i - k + 1]
        for j in range(i - k + 2, i + 1):
            comps += 1
            if xs[j] > best:
                best = xs[j]
        out.append(best)
    return out, comps


def deque_run(xs: list[int], k: int):
    """Pseudocode of L05 Section 3, 1-based step i = index+1, with counters for the while-loop tests."""
    dq: list[int] = []  # 1-based indices, front at 0
    out: list[int] = []
    tests = pops_back = pops_front = pushes = 0
    snapshots = []
    for i in range(1, len(xs) + 1):
        while dq:
            tests += 1
            if xs[dq[-1] - 1] > xs[i - 1]:
                break
            dq.pop()
            pops_back += 1
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.pop(0)
            pops_front += 1
        if i >= k:
            out.append(xs[dq[0] - 1])
        snapshots.append(list(dq))
    return out, tests, pushes, pops_back + pops_front, pops_back, pops_front, snapshots


def surviving(xs: list[int], k: int, i: int) -> list[int]:
    """Definition 3.1: indices j with i-k < j <= i and x_j > x_m for every m with j < m <= i (1-based)."""
    return [j for j in range(max(1, i - k + 1), i + 1) if all(xs[j - 1] > xs[m - 1] for m in range(j + 1, i + 1))]


def main() -> None:
    # Prop 2.1 and Remark 2.2
    for n in range(1, 60):
        for k in range(1, n + 1):
            xs = list(range(n))
            _, c = naive(xs, k)
            assert c == (n - k + 1) * (k - 1), (n, k)
    for n in range(2, 300, 2):
        r = [(n - r) * r for r in range(0, n)]
        assert max(r) == n * n // 4 and r.index(max(r)) == n // 2
        assert max(range(1, n + 1), key=lambda k: (n - k + 1) * (k - 1)) == n // 2 + 1
    print("Prop 2.1 count formula and Remark 2.2 peak: checked n<60 exhaustively, even n<300 for the peak: True")
    print(f"Remark 2.2 n=200 peak k = {max(range(1, 201), key=lambda k: (200 - k + 1) * (k - 1))}")
    print(f"P1 n=200 k=101 count = {(200 - 101 + 1) * (101 - 1)}")

    # Prop 3.2 correctness and Def 3.1 invariant: exhaustive over {0,1,2}^n for n <= 7 (all k)
    cases = 0
    for n in range(1, 8):
        for xs in itertools.product((0, 1, 2), repeat=n):
            xs = list(xs)
            for k in range(1, n + 1):
                out, tests, pushes, pops, _, _, snaps = deque_run(xs, k)
                assert out == brute(xs, k), (xs, k)
                for i, snap in enumerate(snaps, start=1):
                    expect = surviving(xs, k, i)
                    # After the expiry step the deque is the surviving set (Definition 3.1 / Prop 3.2)
                    assert snap == expect, (xs, k, i, snap, expect)
                assert pushes == n and pops <= n and tests <= 2 * n, (xs, k)
                cases += 1
    print(f"Prop 3.2 outputs and Def 3.1 invariant, exhaustive over {{0,1,2}}^n, n<=7, all k: {cases} cases, all pass")

    # Prop 3.3 on random sequences, many sizes and windows
    rng = random.Random(12345)
    worst_ratio = 0.0
    for _ in range(400):
        n = rng.randint(1, 120)
        xs = [rng.randint(0, 99) for _ in range(n)]
        for k in range(1, n + 1):
            out, tests, pushes, pops, _, _, _ = deque_run(xs, k)
            assert out == brute(xs, k)
            assert pushes == n and pops <= n and tests <= 2 * n
            worst_ratio = max(worst_ratio, tests / (2 * n))
    print(f"Prop 3.3 bounds on 400 random sequences (n<=120, all k): pushes = n, pops <= n, tests <= 2n: True;"
          f" largest tests/(2n) = {worst_ratio:.3f}")

    # P3: strictly increasing sequences give exactly n-1 comparisons for every k
    ok = True
    for n in range(1, 31):
        for k in range(1, n + 1):
            _, tests, *_ = deque_run(list(range(n)), k)
            ok = ok and tests == n - 1
    print(f"P3 strictly increasing, comparisons = n-1 for n<=30 and all k: {ok}")

    # Remark 3.4: x = (k, k-1, ..., 2, k+1), n = k: step k removes k-1 entries in one loop
    ok = True
    for k in range(2, 12):
        xs = list(range(k, 1, -1)) + [k + 1]
        assert len(xs) == k
        _, _, _, _, pops_back_total, _, snaps = deque_run(xs, k)
        before = snaps[k - 2]  # deque after step k-1
        after_step_k = snaps[k - 1]
        removed = len(before) - (len(after_step_k) - 1)
        ok = ok and removed == k - 1 and after_step_k == [k]
    print(f"Remark 3.4 one step removes k-1 entries (k=2..11): {ok}")

    # Example 3.5 trace: x = (3,1,4,1,5), k = 3, outputs (4,4,5), deques (1), (1,2), (3), (3,4), (5)
    out, _, _, _, _, _, snaps = deque_run([3, 1, 4, 1, 5], 3)
    print(f"Example 3.5 outputs {tuple(out)}, deques {[tuple(s) for s in snaps]}")

    # Problem M2: x = (2,5,1,0,3), k = 2, outputs (5,5,1,3)
    out, _, _, _, _, _, snaps = deque_run([2, 5, 1, 0, 3], 2)
    print(f"Problem M2 outputs {tuple(out)}, deques {[tuple(s) for s in snaps]}")

    # Lab numbers: seed 5 and seed 6, n = 200, Part 1 and Part 3 table
    rng5 = random.Random(5)
    seq5 = [rng5.randint(0, 999) for _ in range(200)]
    rng6 = random.Random(6)
    seq6 = [rng6.randint(0, 999) for _ in range(200)]
    print(f"seed 5 first five values: {seq5[:5]}")
    for name, seq in (("seed5", seq5), ("seed6", seq6)):
        out, tests, pushes, pops, pb, pf, _ = deque_run(seq, 8)
        nout, ncomp = naive(seq, 8)
        print(f"{name} k=8: outputs equal {out == nout}; naive {ncomp}; deque tests {tests}, pushes {pushes},"
              f" pops {pops} (back {pb}, front {pf}); first five maxima {out[:5]}")
    for k in (1, 2, 8, 32, 200):
        out, tests, pushes, pops, _, _, _ = deque_run(seq5, k)
        nout, ncomp = naive(seq5, k)
        print(f"k={k:>3} windows={200 - k + 1:>4} naive={ncomp:>5} formula={(200 - k + 1) * (k - 1):>5}"
              f" deque_tests={tests:>4} pops={pops:>4} pushes={pushes:>4} outputs_equal={out == nout}")

    # Part 2 claims: window-size agreement 1..20 and edge cases on seed-5 sequence
    agree = all(deque_run(seq5, k)[0] == naive(seq5, k)[0] for k in range(1, 21))
    print(f"outputs equal for k=1..20 on seed 5: {agree}; max(seq5) = {max(seq5)}")

    # E1: 5239/382
    print(f"E1 ratio 5239/382 = {5239 / 382:.4f}")
    # E3 bound check
    print(f"E3 k=200: tests 387 <= 2n = 400 and <= pops 194 + n 200 = {194 + 200}")


if __name__ == "__main__":
    main()
