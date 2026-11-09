"""CS2 L07 lab 1: longest common subsequence and minimum-count coin change, three ways.

SIMULATED: every instance is generated from a fixed seed by an integer generator; none is market data.
Part A: the longest common subsequence (LCS) of 30 seeded string pairs, by memoized recursion, by table fill
and by exhaustive search over all subsequences of the first string. Part B: the fewest coins summing to a
seeded amount, for 30 seeded coin sets, by the same three methods (exhaustive search over all coin-count
vectors), plus the largest-coin-first rule on the coin set (1, 3, 4). Part C: subproblem counts. The memoized
recursion's calls and stored subproblems are counted, the calls of the same recursion with no memo table are
counted, and the table cells filled are counted. The lab counts
operations only; it does not time anything. Standard library only, no network access, no randomness other
than the seeded generator.
"""

from __future__ import annotations

LCG_MULT = 1103515245
LCG_INC = 12345
LCG_MOD = 2**31
SEED = 20261028
ALPHABET = "ACGT"
LCS_INSTANCES = 30
COIN_INSTANCES = 30
FIXED_X = "ACGTACG"
FIXED_Y = "TGCATGC"
FIXED_COINS = (1, 3, 4)
FIXED_AMOUNT = 6
PART_C_AMOUNT = 20


class Lcg:
    """A linear congruential generator on integers, so every run draws the same numbers."""

    def __init__(self, seed: int) -> None:
        self.state = seed % LCG_MOD

    def below(self, n: int) -> int:
        """Return an integer k with 0 <= k < n."""
        if n < 1:
            raise ValueError("below needs n >= 1")
        self.state = (LCG_MULT * self.state + LCG_INC) % LCG_MOD
        return (self.state >> 16) % n


def lcs_memo(x: str, y: str) -> tuple[int, int, int]:
    """LCS length by memoized recursion. Returns (length, distinct subproblems stored, recursive calls)."""
    cache: dict[tuple[int, int], int] = {}
    calls = 0

    def go(i: int, j: int) -> int:
        nonlocal calls
        calls += 1
        if i == 0 or j == 0:
            return 0
        if (i, j) in cache:
            return cache[(i, j)]
        value = go(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(go(i - 1, j), go(i, j - 1))
        cache[(i, j)] = value
        return value

    length = go(len(x), len(y))
    return length, len(cache), calls


def lcs_naive_calls(x: str, y: str) -> int:
    """Recursive calls of the same recursion with no memo table: every call recomputes its subproblem."""
    calls = 0

    def go(i: int, j: int) -> int:
        nonlocal calls
        calls += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))

    go(len(x), len(y))
    return calls


def lcs_table(x: str, y: str) -> tuple[int, int]:
    """LCS length by filling the (m+1) by (n+1) table row by row. Returns (length, cells filled)."""
    m, n = len(x), len(y)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    cells = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cells += 1
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[m][n], cells


def is_subsequence(s: str, t: str) -> bool:
    """True when s can be read off t in order, by deleting symbols of t."""
    remaining = iter(t)
    return all(ch in remaining for ch in s)


def lcs_exhaustive(x: str, y: str) -> int:
    """LCS length by trying every subset of positions of x, which gives every subsequence of x."""
    best = 0
    for mask in range(1 << len(x)):
        s = "".join(x[k] for k in range(len(x)) if (mask >> k) & 1)
        if len(s) > best and is_subsequence(s, y):
            best = len(s)
    return best


def coins_memo(denoms: tuple[int, ...], amount: int) -> tuple[int | None, int, int]:
    """Fewest coins summing to amount, by memoized recursion.

    Returns (fewest coins or None when no combination exists, distinct amounts stored, recursive calls).
    """
    cache: dict[int, int | None] = {}
    calls = 0

    def best(a: int) -> int | None:
        nonlocal calls
        calls += 1
        if a == 0:
            return 0
        if a in cache:
            return cache[a]
        found: list[int] = []
        for c in denoms:
            if c <= a:
                sub = best(a - c)
                if sub is not None:
                    found.append(1 + sub)
        value = min(found) if found else None
        cache[a] = value
        return value

    answer = best(amount)
    return answer, len(cache), calls


def coins_naive_calls(denoms: tuple[int, ...], amount: int) -> int:
    """Recursive calls of the same recursion with no memo table."""
    calls = 0

    def best(a: int) -> int | None:
        nonlocal calls
        calls += 1
        if a == 0:
            return 0
        found: list[int] = []
        for c in denoms:
            if c <= a:
                sub = best(a - c)
                if sub is not None:
                    found.append(1 + sub)
        return min(found) if found else None

    best(amount)
    return calls


def coins_table(denoms: tuple[int, ...], amount: int) -> tuple[int | None, int]:
    """Fewest coins by filling the table entry for each amount 0..amount. Returns (answer, entries filled)."""
    table: list[int | None] = [0] + [None] * amount
    for a in range(1, amount + 1):
        found: list[int] = []
        for c in denoms:
            sub = table[a - c] if c <= a else None
            if sub is not None:
                found.append(1 + sub)
        table[a] = min(found) if found else None
    return table[amount], amount


def coins_exhaustive(denoms: tuple[int, ...], amount: int) -> int | None:
    """Fewest coins by trying every vector of coin counts (k_1, ..., k_d) with sum k_i * d_i = amount."""
    best: int | None = None

    def search(k: int, remaining: int, used: int) -> None:
        nonlocal best
        if k == len(denoms):
            if remaining == 0 and (best is None or used < best):
                best = used
            return
        c = denoms[k]
        for count in range(remaining // c + 1):
            search(k + 1, remaining - count * c, used + count)

    search(0, amount, 0)
    return best


def greedy_count(denoms: tuple[int, ...], amount: int) -> int | None:
    """Largest-coin-first: repeatedly take the largest coin that fits. Returns the number of coins used."""
    remaining, used = amount, 0
    while remaining > 0:
        fits = [c for c in denoms if c <= remaining]
        if not fits:
            return None
        remaining -= max(fits)
        used += 1
    return used


def make_lcs_instances(gen: Lcg) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for _ in range(LCS_INSTANCES):
        m = 1 + gen.below(7)
        n = 1 + gen.below(7)
        x = "".join(ALPHABET[gen.below(len(ALPHABET))] for _ in range(m))
        y = "".join(ALPHABET[gen.below(len(ALPHABET))] for _ in range(n))
        pairs.append((x, y))
    return pairs


def make_coin_instances(gen: Lcg) -> list[tuple[tuple[int, ...], int]]:
    cases: list[tuple[tuple[int, ...], int]] = []
    for _ in range(COIN_INSTANCES):
        size = 2 + gen.below(3)
        chosen: set[int] = set()
        while len(chosen) < size:
            chosen.add(1 + gen.below(9))
        amount = gen.below(13)
        cases.append((tuple(sorted(chosen)), amount))
    return cases


def part_a(pairs: list[tuple[str, str]]) -> None:
    for x, y in pairs:
        memo, _, _ = lcs_memo(x, y)
        table, cells = lcs_table(x, y)
        exact = lcs_exhaustive(x, y)
        if not memo == table == exact:
            raise AssertionError(f"LCS methods disagree on {x!r}, {y!r}: {memo}, {table}, {exact}")
        if cells != len(x) * len(y):
            raise AssertionError(f"table fill did not fill m * n cells for {x!r}, {y!r}")
    print(f"part A: LCS instances checked: {len(pairs)}; memo, table and exhaustive agree on all of them")
    x, y = pairs[0]
    print(f"part A: first instance x = {x}, y = {y}, LCS length = {lcs_table(x, y)[0]}")


def part_b(cases: list[tuple[tuple[int, ...], int]]) -> None:
    for denoms, amount in cases:
        memo, _, _ = coins_memo(denoms, amount)
        table, _ = coins_table(denoms, amount)
        exact = coins_exhaustive(denoms, amount)
        if not memo == table == exact:
            raise AssertionError(f"coin methods disagree on {denoms}, {amount}: {memo}, {table}, {exact}")
    impossible = sum(1 for denoms, amount in cases if coins_table(denoms, amount)[0] is None)
    print(f"part B: coin instances checked: {len(cases)}; memo, table and exhaustive agree on all of them")
    print(f"part B: instances with no combination (answer None): {impossible} of {len(cases)}")
    greedy = greedy_count(FIXED_COINS, FIXED_AMOUNT)
    optimum = coins_table(FIXED_COINS, FIXED_AMOUNT)[0]
    print(
        f"part B: coins {FIXED_COINS}, amount {FIXED_AMOUNT}: "
        f"largest-coin-first uses {greedy} coins, optimum uses {optimum}"
    )


def part_c() -> None:
    memo, stored, calls = lcs_memo(FIXED_X, FIXED_Y)
    _, cells = lcs_table(FIXED_X, FIXED_Y)
    naive = lcs_naive_calls(FIXED_X, FIXED_Y)
    if stored > len(FIXED_X) * len(FIXED_Y):
        raise AssertionError("more stored subproblems than table cells")
    print(f"part C: LCS x = {FIXED_X}, y = {FIXED_Y}, LCS length = {memo}")
    print(f"part C: table cells filled = {cells}; memo subproblems stored = {stored}; memo calls = {calls}")
    print(f"part C: recursion with no memo table makes {naive} calls")
    coin_memo, stored_c, calls_c = coins_memo(FIXED_COINS, PART_C_AMOUNT)
    naive_c = coins_naive_calls(FIXED_COINS, PART_C_AMOUNT)
    print(f"part C: coins {FIXED_COINS}, amount {PART_C_AMOUNT}: fewest coins = {coin_memo}")
    print(
        f"part C: amounts stored = {stored_c}; memo calls = {calls_c}; "
        f"recursion with no memo table makes {naive_c} calls"
    )


def main() -> None:
    gen = Lcg(SEED)
    pairs = make_lcs_instances(gen)
    cases = make_coin_instances(gen)
    part_a(pairs)
    part_b(cases)
    part_c()


main()
