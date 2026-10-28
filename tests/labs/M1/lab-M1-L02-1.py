"""M1 lab L02: a direct proof checked on a finite range, and a contradiction proof with a search.

Standard library only. No randomness and no network. Each claim is tested on a finite range,
which is evidence about that range. The proofs on the page are what establish the claims for
all integers. The searches below can only find counterexamples, and the page reads the output
that way.
"""

from __future__ import annotations

from math import gcd


def is_even(n: int) -> bool:
    """True when n = 2k for some integer k."""
    return n % 2 == 0


def direct_proof_cases(bound: int) -> tuple[int, int, int, int]:
    """Test the direct-proof claim for even a, b in -bound..bound.

    Claim: if a and b are even, then a + b is even and a * b is divisible by 4.
    The proof writes a = 2m and b = 2n, so a + b = 2(m + n) and a * b = 4mn. The code uses
    exactly those witnesses m = a // 2 and n = b // 2, and checks both identities for each pair.

    Returns (pairs tested, conclusion holds, identities hold, pairs where the conclusion fails).
    """
    evens = [n for n in range(-bound, bound + 1) if is_even(n)]
    tested = conclusion = identities = 0
    for a in evens:
        for b in evens:
            m, n = a // 2, b // 2
            tested += 1
            if is_even(a + b) and (a * b) % 4 == 0:
                conclusion += 1
            if a + b == 2 * (m + n) and a * b == 4 * m * n:
                identities += 1
    return tested, conclusion, identities, tested - conclusion


def refute_by_search(bound: int) -> int:
    """The least even a in 0..bound for which a * a + 1 is even, or -1 if none exists in range.

    The claim 'if a is even, then a * a + 1 is even' is false. A search finds a counterexample;
    it cannot show a claim is true.
    """
    for a in range(0, bound + 1, 2):
        if not is_even(a * a + 1):
            return a
    return -1


def parity_lemma(bound: int) -> tuple[int, int, bool]:
    """Lemma used in the contradiction proof: for integers p, if p * p is even then p is even.

    Returns (count of p in -bound..bound with p * p even, count with p even, the two sets are equal).
    """
    values = range(-bound, bound + 1)
    square_even = [p for p in values if is_even(p * p)]
    even = [p for p in values if is_even(p)]
    return len(square_even), len(even), square_even == even


def search_square_equation(c: int, q_max: int, p_max: int) -> tuple[int, int, int]:
    """Count integer solutions of p * p == c * q * q with 1 <= q <= q_max and |p| <= p_max.

    Returns (tested pairs, solutions, solutions with gcd(p, q) = 1).
    """
    tested = solutions = coprime = 0
    for q in range(1, q_max + 1):
        for p in range(-p_max, p_max + 1):
            tested += 1
            if p * p == c * q * q:
                solutions += 1
                if gcd(abs(p), q) == 1:
                    coprime += 1
    return tested, solutions, coprime


def main() -> None:
    tested, conclusion, identities, failed = direct_proof_cases(60)
    print(f"direct proof, a and b even in -60 to 60: pairs tested {tested}")
    print(f"a + b even and a * b divisible by 4: {conclusion} of {tested} pairs")
    print(f"witness identities a + b = 2(m + n) and a * b = 4mn: {identities} of {tested} pairs")
    print(f"pairs where the conclusion fails: {failed}")
    counterexample = refute_by_search(60)
    print(f"refutation of 'a even implies a*a + 1 even' over even a in 0 to 60: least counterexample {counterexample}")

    square_even, even, same = parity_lemma(2000)
    print(f"parity lemma, p in -2000 to 2000: p*p even for {square_even} values, p even for {even} values")
    print(f"the two sets of values are equal: {same}")

    tested, solutions, coprime = search_square_equation(2, 300, 500)
    print(f"search p*p == 2*q*q, 1 <= q <= 300, |p| <= 500: pairs tested {tested}")
    print(f"solutions found: {solutions}")
    tested, solutions, coprime = search_square_equation(4, 300, 500)
    print(f"search p*p == 4*q*q over the same range: solutions {solutions}, with gcd(p, q) = 1: {coprime}")


main()
