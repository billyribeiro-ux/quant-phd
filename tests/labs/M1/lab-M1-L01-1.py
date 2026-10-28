"""M1 lab L01: quantified statements over finite domains, checked by exhaustive enumeration.

Standard library only. No randomness and no network: every case is enumerated, so the output is
the same on every run. A check over a finite domain tests that domain only. It is evidence about
the finite case and says nothing about an infinite domain, and the page reads the output that way.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from itertools import product

Pred1 = Callable[[int], bool]
Pred2 = Callable[[int, int], bool]


def forall(domain: Iterable[int], pred: Pred1) -> bool:
    """True when pred(x) holds for every x in domain. An empty domain gives True."""
    return all(pred(x) for x in domain)


def exists(domain: Iterable[int], pred: Pred1) -> bool:
    """True when pred(x) holds for at least one x in domain. An empty domain gives False."""
    return any(pred(x) for x in domain)


def negated(pred: Pred1) -> Pred1:
    """The predicate x -> not pred(x)."""

    def result(x: int) -> bool:
        return not pred(x)

    return result


def table_predicate(table: dict[int, bool]) -> Pred1:
    """The predicate given by a table of truth values, one per member of its domain."""

    def result(x: int) -> bool:
        return table[x]

    return result


def smallest_factor(n: int) -> int:
    """The least divisor d >= 2 of n >= 2, found by trial division. Input outside n >= 2 raises ValueError."""
    if n < 2:
        raise ValueError(f"smallest_factor needs n >= 2, got {n}")
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n


def is_prime(n: int) -> bool:
    """True when n is a prime number. Integers below 2 are not prime."""
    return n >= 2 and smallest_factor(n) == n


def negation_check(domain: Sequence[int]) -> tuple[int, int]:
    """Count the predicates on domain for which not-forall agrees with exists-not, and the predicates tested.

    A predicate on a finite domain is an assignment of True or False to each element, so there are
    2 to the power len(domain) of them. Each one is tested.
    """
    tested = 0
    agree = 0
    for values in product((False, True), repeat=len(domain)):
        pred = table_predicate(dict(zip(domain, values, strict=True)))
        tested += 1
        left = not forall(domain, pred)
        right = exists(domain, negated(pred))
        agree += left == right
    return agree, tested


def forall_exists(rel: dict[tuple[int, int], bool], domain: Sequence[int]) -> bool:
    """True when for every x in domain some y in domain has R(x, y), with R given as a table."""
    return all(any(rel[(x, y)] for y in domain) for x in domain)


def exists_forall(rel: dict[tuple[int, int], bool], domain: Sequence[int]) -> bool:
    """True when some x in domain has R(x, y) for every y in domain, with R given as a table."""
    return any(all(rel[(x, y)] for y in domain) for x in domain)


def relation_check(size: int) -> tuple[int, int, int, int]:
    """Over binary relations R on {0, ..., size-1}, test two quantifier identities and count one property.

    Returns (agree_1, agree_2, total, count_forall_exists), where:
      agree_1: cases where not(forall x exists y R(x,y)) equals (exists x forall y not R(x,y));
      agree_2: cases where not(exists x forall y R(x,y)) equals (forall x exists y not R(x,y));
      total: the number of relations, 2 to the power size*size;
      count_forall_exists: relations with forall x exists y R(x,y).
    """
    domain = range(size)
    cells = [(x, y) for x in domain for y in domain]
    agree_1 = agree_2 = count = total = 0
    for bits in product((False, True), repeat=len(cells)):
        rel = dict(zip(cells, bits, strict=True))
        total += 1
        fe = forall_exists(rel, domain)
        ef = exists_forall(rel, domain)
        count += fe
        agree_1 += (not fe) == any(all(not rel[(x, y)] for y in domain) for x in domain)
        agree_2 += (not ef) == all(any(not rel[(x, y)] for y in domain) for x in domain)
    return agree_1, agree_2, total, count


def order_matters() -> tuple[bool, bool]:
    """On Z_5 with R(x, y) meaning y = x + 1 (mod 5): forall x exists y R, and exists y forall x R."""
    domain = range(5)

    def r(x: int, y: int) -> bool:
        return y == (x + 1) % 5

    forall_exists = forall(domain, lambda x: exists(domain, lambda y: r(x, y)))
    exists_forall = exists(domain, lambda y: forall(domain, lambda x: r(x, y)))
    return forall_exists, exists_forall


def first_non_prime(limit: int) -> tuple[int, int, int]:
    """The least n in 1..limit with n*n + n + 41 not prime, with the value and its smallest factor.

    Returns (n, value, smallest factor), or (0, 0, 0) if no n in range fails.
    """
    for n in range(1, limit + 1):
        value = n * n + n + 41
        if not is_prime(value):
            return n, value, smallest_factor(value)
    return 0, 0, 0


def main() -> None:
    d4 = [0, 1, 2, 3]
    agree, tested = negation_check(d4)
    print(f"domain {{0, 1, 2, 3}}: predicates tested {tested}")
    print(f"not-forall equals exists-not on {agree} of {tested} predicates")

    a1, a2, total, count = relation_check(3)
    print("domain {0, 1, 2}: binary relations tested", total)
    print(f"not-forall-exists equals exists-forall-not on {a1} of {total} relations")
    print(f"not-exists-forall equals forall-exists-not on {a2} of {total} relations")
    print(f"relations with forall x exists y R(x, y): {count}")

    fe, ef = order_matters()
    print("domain Z_5, R(x, y) meaning y = x + 1 mod 5")
    print(f"forall x exists y R(x, y): {fe}")
    print(f"exists y forall x R(x, y): {ef}")

    primes = sum(is_prime(n * n + n + 41) for n in range(1, 40))
    print(f"n from 1 to 39 with n*n + n + 41 prime: {primes} of 39")
    n, value, factor = first_non_prime(50)
    print(f"least n in 1 to 50 with n*n + n + 41 not prime: {n}")
    print(f"value at that n: {value} = {factor} x {value // factor}")

    stmt = forall(range(1, 11), lambda x: x * x >= x)
    print(f"statement for every x in 1 to 10, x*x >= x: {stmt}")


main()
