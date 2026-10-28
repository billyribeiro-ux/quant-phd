"""CS2 lab L04: comparison counts of two sorts, the comparison lower bound, and binary-search probes.

SIMULATED inputs: Parts A and B use permutations of 0..n-1 drawn from a seeded generator (seed
20261028); Parts C and D use sorted lists of integers that the code builds.
No market data, no network, standard library only. Every count is a number of key comparisons. No time is
measured, so every run prints the same lines.

Part A: comparisons of insertion sort and merge sort on seeded random permutations, and on sorted input.
Part B: the worst case over every permutation of n = 2 to 7, checked against the lower bound
ceil(log2 n!) for any comparison sort and the merge-sort bound n * ceil(log2 n).
Part C: the inequality log2(n!) >= (n/2) log2(n/2) for 2 <= n <= 1000, on floats with the margin printed.
Part D: unsuccessful binary-search probes over all n + 1 gaps of a sorted list of n values, for every n from
1 to 1000, compared with floor(log2 n) + 1, which equals n.bit_length().
"""

from __future__ import annotations

import itertools
import math
import random

SEED = 20261028


def insertion_sort(xs: list[int]) -> tuple[list[int], int]:
    """Sort a copy of xs by insertion. Returns the sorted list and the number of key comparisons."""
    a = list(xs)
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a, comparisons


def merge_sort(xs: list[int]) -> tuple[list[int], int]:
    """Sort a copy of xs by merge sort. Returns the sorted list and the number of key comparisons."""
    if len(xs) <= 1:
        return list(xs), 0
    mid = len(xs) // 2
    left, count_left = merge_sort(xs[:mid])
    right, count_right = merge_sort(xs[mid:])
    merged: list[int] = []
    comparisons = count_left + count_right
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, comparisons


def ceil_log2(n: int) -> int:
    """The least integer c with 2^c >= n, for an integer n >= 1. Exact, by integer arithmetic."""
    return (n - 1).bit_length()


def probes_unsuccessful(sorted_values: list[int], key: int) -> int:
    """Probes of binary search for key, which is absent, with midpoint (lo + hi) // 2 over 0..len-1."""
    lo = 0
    hi = len(sorted_values) - 1
    probes = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        probes += 1
        if sorted_values[mid] == key:
            return probes
        if sorted_values[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return probes


def gap_queries(n: int) -> list[int]:
    """n + 1 absent keys for the list 0, 2, ..., 2(n-1): one below the first value, one in each gap, one above."""
    return [-1] + [2 * i + 1 for i in range(n - 1)] + [2 * (n - 1) + 1]


def part_a(rng: random.Random) -> None:
    print("Part A: comparisons on seeded random permutations, and on sorted input")
    print("n  insertion_comparisons  merge_comparisons  merge_bound_n_ceil_log2_n")
    for n in (8, 64, 256, 1024):
        xs = list(range(n))
        rng.shuffle(xs)
        ins, c_ins = insertion_sort(xs)
        mer, c_mer = merge_sort(xs)
        if ins != sorted(xs) or mer != sorted(xs):
            raise AssertionError(f"a sort returned a wrong order at n = {n}")
        print(f"{n} {c_ins} {c_mer} {n * ceil_log2(n)}")
    n = 1024
    ascending = list(range(n))
    _, c_ins_sorted = insertion_sort(ascending)
    _, c_mer_sorted = merge_sort(ascending)
    print(f"sorted input n={n}: insertion_comparisons {c_ins_sorted} merge_comparisons {c_mer_sorted}")
    print(f"insertion_fewer_on_sorted_input {c_ins_sorted < c_mer_sorted}")
    print(f"lower_bound_ceil_log2_factorial_n {ceil_log2(math.factorial(n))}")
    print(f"merge_sorted_input_below_lower_bound {c_mer_sorted < ceil_log2(math.factorial(n))}")


def part_b() -> None:
    print("Part B: worst case over every permutation of n = 2 to 7")
    print("n  permutations  max_insertion  max_merge  lower_ceil_log2_n_factorial  merge_bound_n_ceil_log2_n")
    for n in range(2, 8):
        max_ins = 0
        max_mer = 0
        count = 0
        for perm in itertools.permutations(range(n)):
            count += 1
            xs = list(perm)
            ins, c_ins = insertion_sort(xs)
            mer, c_mer = merge_sort(xs)
            if ins != sorted(xs) or mer != sorted(xs):
                raise AssertionError(f"a sort returned a wrong order for {xs}")
            max_ins = max(max_ins, c_ins)
            max_mer = max(max_mer, c_mer)
        lower = ceil_log2(math.factorial(n))
        upper = n * ceil_log2(n)
        print(f"{n} {count} {max_ins} {max_mer} {lower} {upper}")
        print(
            f"checks n={n}: insertion_max_is_n_choose_2 {max_ins == n * (n - 1) // 2} "
            f"merge_max_at_least_lower {max_mer >= lower} merge_max_at_most_upper {max_mer <= upper}"
        )


def part_c() -> None:
    print("Part C: log2(n!) >= (n/2) log2(n/2) for 2 <= n <= 1000")
    ln2 = math.log(2.0)
    holds = True
    smallest_margin = math.inf
    smallest_n = 0
    for n in range(2, 1001):
        lhs = math.lgamma(n + 1) / ln2
        rhs = (n / 2) * math.log2(n / 2)
        holds = holds and lhs >= rhs
        if lhs - rhs < smallest_margin:
            smallest_margin = lhs - rhs
            smallest_n = n
    print(f"inequality_holds_for_2_to_1000 {holds}")
    print(f"smallest_margin_at_n {smallest_n} margin {smallest_margin:.6f}")
    for n in (2, 3, 4, 10, 100, 1000):
        lhs = math.lgamma(n + 1) / ln2
        rhs = (n / 2) * math.log2(n / 2)
        print(f"n {n} log2_factorial {lhs:.4f} half_n_log2_half_n {rhs:.4f}")


def part_d() -> None:
    print("Part D: unsuccessful binary-search probes over all n + 1 gaps, for n = 1 to 1000")
    all_match = True
    total_gaps = 0
    for n in range(1, 1001):
        values = [2 * i for i in range(n)]
        worst = 0
        for key in gap_queries(n):
            worst = max(worst, probes_unsuccessful(values, key))
            total_gaps += 1
        if worst != n.bit_length():
            all_match = False
        if n in (1, 2, 3, 4, 7, 8, 15, 16, 1000):
            print(f"n {n} worst_probes {worst} floor_log2_n_plus_1 {n.bit_length()}")
    print(f"gaps_checked {total_gaps}")
    print(f"worst_equals_floor_log2_n_plus_1_for_every_n_1_to_1000 {all_match}")


def main() -> None:
    rng = random.Random(SEED)
    part_a(rng)
    part_b()
    part_c()
    part_d()


main()
