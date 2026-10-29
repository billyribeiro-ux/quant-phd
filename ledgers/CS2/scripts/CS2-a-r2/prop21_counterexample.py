"""L04 Proposition 2.1 hypotheses (1)-(4) as printed on the page, with a no-comparison algorithm that is
deterministic, halts, uses no key operation at all, and admits every ordering. Its comparison count (0) is below
ceil(log2 n!) for n >= 2, and its output is not sorted, so the proposition as printed does not hold for it."""
import itertools
import math


def do_nothing(xs):
    """Returns its input unchanged. Makes zero comparisons (a deterministic, halting algorithm)."""
    return list(xs), 0


for n in range(2, 8):
    lower = math.ceil(math.log2(math.factorial(n)))
    orders = list(itertools.permutations(range(n)))
    comparisons = max(do_nothing(p)[1] for p in orders)
    unsorted = sum(1 for p in orders if do_nothing(p)[0] != sorted(p))
    print(f"n={n} lower_ceil_log2_n_factorial={lower} max_comparisons_of_do_nothing={comparisons} "
          f"orderings_not_sorted={unsorted} of {len(orders)} counterexample={comparisons < lower}")
