"""PC3 lab L02: a seeded drill set of generated items, Monty Hall under two host rules, and a Bayes check.

Standard library only. The drill items are generated from random.Random(SEED), so the same seed gives the same
items on every run. Each item's exact answer is computed twice: by counting the outcomes of every sequence of
flips (exact enumeration) and by a closed-form formula. The score counts the items on which the two agree. The
items are generated items, not data, and no file is read. Every probability is a fractions.Fraction.

Part 2 enumerates every (car door, picked door, host door) triple. Part 3 enumerates every (bag, colour) pair.
Part 4 enumerates two fair coins and every ordered pair of balls drawn without replacement from an urn. A finite
enumeration computes each stated probability exactly. The lab does not estimate any probability by simulation.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

SEED = 0
ITEM_COUNT = 12
DOORS = (0, 1, 2)


@dataclass(frozen=True)
class Item:
    """One drill item: the event, the number of flips, and the parameter of the event."""

    number: int
    text: str
    flips: int
    kind: str  # "at-least" or "first-head"
    arg: int


def make_items(seed: int, count: int) -> list[Item]:
    """Generate count drill items from the seed. Each item has 3 to 8 fair flips."""
    rng = random.Random(seed)
    items: list[Item] = []
    for number in range(1, count + 1):
        flips = rng.randint(3, 8)
        if rng.random() < 0.5:
            k = rng.randint(1, flips)
            noun = "head" if k == 1 else "heads"
            text = f"at least {k} {noun} in {flips} fair flips"
            items.append(Item(number, text, flips, "at-least", k))
        else:
            j = rng.randint(1, flips)
            text = f"the first head on flip {j} of {flips} fair flips"
            items.append(Item(number, text, flips, "first-head", j))
    return items


def enumerate_probability(item: Item) -> Fraction:
    """The exact probability of the item's event, by counting all 2^flips equally likely sequences."""
    favourable = 0
    for seq in product((0, 1), repeat=item.flips):
        heads = sum(seq)
        if item.kind == "at-least":
            hit = heads >= item.arg
        else:
            hit = seq[item.arg - 1] == 1 and all(s == 0 for s in seq[: item.arg - 1])
        favourable += hit
    return Fraction(favourable, 2**item.flips)


def closed_form(item: Item) -> Fraction:
    """The same probability from the formulas: a binomial tail, or 1/2^j for the first head on flip j."""
    if item.kind == "at-least":
        return Fraction(sum(math.comb(item.flips, i) for i in range(item.arg, item.flips + 1)), 2**item.flips)
    return Fraction(1, 2**item.arg)


def part_one() -> None:
    print(f"Part 1 · drill set from seed {SEED}, {ITEM_COUNT} generated items")
    items = make_items(SEED, ITEM_COUNT)
    agree = 0
    for item in items:
        exact = enumerate_probability(item)
        formula = closed_form(item)
        same = exact == formula
        agree += same
        print(f"item {item.number:2d}: {item.text}: probability {exact}, formula {formula}, equal {same}")
    print(f"closed form equals enumeration on {agree} of {len(items)} items")


def switch_probabilities(rule: str) -> tuple[Fraction, Fraction]:
    """Stay and switch win probabilities, given that the host has opened a goat door.

    rule "always-goat": the host always opens a goat door among the doors not picked (a uniform choice when
    two goat doors remain). rule "random": the host opens one of the two unpicked doors uniformly at random,
    and the outcomes in which that door hides the car are discarded, which conditions on a goat being revealed.
    """
    stay = Fraction(0)
    switch = Fraction(0)
    total = Fraction(0)
    for car, pick in product(DOORS, DOORS):
        others = [d for d in DOORS if d != pick]
        for opened in others:
            if rule == "always-goat":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                p_open = Fraction(1, len(goats))
            elif rule == "random":
                if opened == car:
                    continue
                p_open = Fraction(1, 2)
            else:
                raise ValueError(f"unknown host rule {rule!r}")
            weight = Fraction(1, 3) * Fraction(1, 3) * p_open
            total += weight
            switch_door = next(d for d in others if d != opened)
            if pick == car:
                stay += weight
            if switch_door == car:
                switch += weight
    return stay / total, switch / total


def part_two() -> None:
    print("Part 2 · Monty Hall, exact enumeration of (car, pick, host door)")
    stay_a, switch_a = switch_probabilities("always-goat")
    print(f"host always opens a goat door: P(stay wins) = {stay_a}, P(switch wins) = {switch_a}")
    stay_b, switch_b = switch_probabilities("random")
    print(f"host opens at random, given a goat: P(stay wins) = {stay_b}, P(switch wins) = {switch_b}")
    print(f"the two host rules give different answers: {switch_a != switch_b}")


def part_three() -> None:
    print("Part 3 · Bayes' rule on two bags, exact enumeration of (bag, colour)")
    bags = {"bag 1": (3, 1), "bag 2": (1, 3)}  # (red, blue) counts
    joint: dict[tuple[str, str], Fraction] = {}
    for bag, (red, blue) in bags.items():
        n = red + blue
        joint[(bag, "red")] = Fraction(1, 2) * Fraction(red, n)
        joint[(bag, "blue")] = Fraction(1, 2) * Fraction(blue, n)
    p_red = sum(v for (_, colour), v in joint.items() if colour == "red")
    posterior = joint[("bag 1", "red")] / p_red
    print(f"P(red) = {p_red}")
    print(f"P(bag 1 | red) by enumeration = {posterior}")
    prior = Fraction(1, 2)
    likelihood = Fraction(3, 4)
    print(f"P(bag 1 | red) by Bayes' rule = {likelihood * prior / p_red}")


def conditional(
    outcomes: Sequence[tuple[str, ...]],
    event: Callable[[tuple[str, ...]], bool],
    given: Callable[[tuple[str, ...]], bool],
) -> Fraction:
    """P(event | given) over equally likely outcomes: the count of both over the count of the given event."""
    kept = [o for o in outcomes if given(o)]
    both = [o for o in kept if event(o)]
    return Fraction(len(both), len(kept))


def part_four() -> None:
    print("Part 4 · two fair coins and an urn, exact enumeration")
    coins = list(product(("H", "T"), repeat=2))  # four equally likely outcomes
    p_both_given_one = conditional(coins, lambda o: o == ("H", "H"), lambda o: "H" in o)
    p_both_given_first = conditional(coins, lambda o: o == ("H", "H"), lambda o: o[0] == "H")
    p_one_given_both = conditional(coins, lambda o: "H" in o, lambda o: o == ("H", "H"))
    print(f"P(both heads | at least one head) = {p_both_given_one}")
    print(f"P(both heads | first flip heads) = {p_both_given_first}")
    print(f"P(at least one head | both heads) = {p_one_given_both}")
    p_both = Fraction(sum(o == ("H", "H") for o in coins), len(coins))
    print(f"P(both heads) = {p_both}")
    balls = ("r1", "r2", "r3", "b1", "b2")
    pairs = [(a, b) for a in balls for b in balls if a != b]  # 20 equally likely ordered draws
    red = {"r1", "r2", "r3"}
    p_second_red = Fraction(sum(b in red for _, b in pairs), len(pairs))
    p_first_red = Fraction(sum(a in red for a, _ in pairs), len(pairs))
    p_both_red = Fraction(sum(a in red and b in red for a, b in pairs), len(pairs))
    print(f"P(second red) = {p_second_red}")
    print(f"P(first red) = {p_first_red}")
    print(f"P(first red and second red) = {p_both_red}")
    print(f"P(second red) equals P(first red): {p_second_red == p_first_red}")
    p_red_given_blue = conditional(pairs, lambda o: o[1] in red, lambda o: o[0] == "b1" or o[0] == "b2")
    print(f"P(second red | first blue) = {p_red_given_blue}")


def main() -> None:
    part_one()
    part_two()
    part_three()
    part_four()


main()
