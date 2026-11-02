"""Scan n = 1..20000 for the n where a float index differs from the exact (99n+99)//100 index (verifier round 1)."""

from __future__ import annotations

import math


def exact_index(n: int) -> int:
    return (99 * n + 99) // 100


def float_index(n: int) -> int:
    return math.ceil(0.99 * n)


def round_index(n: int) -> int:
    return round(0.99 * n)


def main() -> None:
    float_bad = [n for n in range(1, 20001) if float_index(n) != exact_index(n)]
    round_bad = [n for n in range(1, 20001) if round_index(n) != exact_index(n)]
    print("float ceil(0.99 n) differs from exact at", len(float_bad), "n in 1..20000; first 12:", float_bad[:12])
    print("round(0.99 n) differs from exact at", len(round_bad), "n in 1..20000; first 12:", round_bad[:12])
    print("float at n = 100:", float_index(100), exact_index(100))
    print("float at n = 6003:", float_index(6003), exact_index(6003))
    print("float at n = 9997:", float_index(9997), exact_index(9997))
    print("float at n = 19987:", float_index(19987), exact_index(19987))
    print("round at n = 99:", round_index(99), exact_index(99))
    print("round at n = 9997:", round_index(9997), exact_index(9997))
    print("round at n = 19987:", round_index(19987), exact_index(19987))


if __name__ == "__main__":
    main()
