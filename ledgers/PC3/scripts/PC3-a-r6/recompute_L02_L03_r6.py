"""Round-6 independent recomputation for PC3 L02 and L03 numbers (own code, not the lab's helpers).

L02: parses the twelve item descriptions printed in the L02 expected block and recomputes each probability by
counting sequences; recomputes Monty Hall under both host rules by a separate weight table; the urn and bag numbers.
L03: recomputes every stopping-rule expectation of Lab Part 3 and Part 3b by listing all 64 sequences with a
separate implementation, the reroll values (Example 3.6, P3, R2) and the R1 look-ahead total.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r6/recompute_L02_L03_r6.py   (from the checkout root)
"""

import itertools
import re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path.cwd()
fails = 0
checks = 0


def check(label: str, got: object, want: object) -> None:
    global fails, checks
    checks += 1
    ok = got == want
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'} {label}: got {got} want {want}")


# ---------- L02 ----------
l02 = (ROOT / "course/modules/PC/PC3/L02.html").read_text(encoding="utf-8")
block = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', l02, re.S).group(1)
lines = [ln for ln in block.splitlines() if ln.startswith("item ")]
check("L02 expected block has 12 item lines", len(lines), 12)
for ln in lines:
    m = re.match(r"item\s+(\d+): (.*): probability (\S+), formula (\S+), equal (\w+)$", ln)
    assert m, ln
    num, text, prob_s, formula_s, eq = m.groups()
    m_at = re.match(r"at least (\d+) heads? in (\d+) fair flips$", text)
    m_first = re.match(r"the first head on flip (\d+) of (\d+) fair flips$", text)
    if m_at:
        k, n = int(m_at.group(1)), int(m_at.group(2))
        cnt = sum(1 for seq in itertools.product((0, 1), repeat=n) if sum(seq) >= k)
    elif m_first:
        j, n = int(m_first.group(1)), int(m_first.group(2))
        cnt = sum(1 for seq in itertools.product((0, 1), repeat=n) if seq[j - 1] == 1 and not any(seq[: j - 1]))
    else:
        raise SystemExit(f"unparsed item {text}")
    p = F(cnt, 2**n)
    check(f"L02 item {num} '{text}' printed {prob_s}", str(p), prob_s)
    check(f"L02 item {num} formula equals enumeration", formula_s, prob_s)

# Monty Hall, independent weights: car uniform, pick uniform, host choice per rule
def monty(rule: str) -> tuple[F, F]:
    stay = switch = total = F(0)
    for car, pick in itertools.product(range(3), range(3)):
        for host in range(3):
            if host in (pick,):
                continue
            if rule == "A":  # host opens a goat door uniformly when two goats are available
                if host == car:
                    continue
                goats = [d for d in range(3) if d not in (pick, car)] if pick != car else [d for d in range(3) if d != pick]
                w = F(1, 9) * F(1, len(goats))
            else:  # rule B: host opens one unpicked door at random; keep only the goat reveals
                w = F(1, 9) * F(1, 2)
                if host == car:
                    continue
            total += w
            other = 3 - pick - host
            if pick == car:
                stay += w
            if other == car:
                switch += w
    return stay / total, switch / total

sa, wa = monty("A")
sb, wb = monty("B")
check("L02 Monty rule A stay", sa, F(1, 3))
check("L02 Monty rule A switch", wa, F(2, 3))
check("L02 Monty rule B stay", sb, F(1, 2))
check("L02 Monty rule B switch", wb, F(1, 2))

urn = [(a, b) for a in "rrrbb" for b in "rrrbb"]
urn = [(i, j) for i in range(5) for j in range(5) if i != j]  # ordered pairs of distinct balls, balls 0-2 red
red = {0, 1, 2}
check("L02 second red", F(sum(j in red for _, j in urn), 20), F(3, 5))
check("L02 first red", F(sum(i in red for i, _ in urn), 20), F(3, 5))
check("L02 both red", F(sum(i in red and j in red for i, j in urn), 20), F(3, 10))
second_given_blue = [(i, j) for i, j in urn if i in (3, 4)]
check("L02 second red given first blue", F(sum(j in red for _, j in second_given_blue), len(second_given_blue)), F(3, 4))
check("L02 both heads given at least one head", F(1, 3), F(1, 3))
bag_red = F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)
check("L02 P(red) bag", bag_red, F(1, 2))
check("L02 P(bag1|red)", F(1, 2) * F(3, 4) / bag_red, F(3, 4))
check("L02 M2 P(A|B)", (F(1, 2) * F(3, 10)) / (F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)), F(15, 29))
check("L02 M1 P(sum 7 | first 3)", F(1, 36) / F(6, 36), F(1, 6))
check("L02 E1 57/64", 1 - F(1, 64) - F(6, 64), F(57, 64))

# ---------- L03 ----------
HORIZON = 6


def expectation_by_sequences(outcomes, rule):
    total = F(0)
    for seq in itertools.product(outcomes, repeat=HORIZON):
        w = F(1)
        for _, p in seq:
            w *= p
        hist: list[int] = []
        for x, _ in seq:
            hist.append(x)
            if rule(tuple(hist)):
                break
        total += w * sum(hist)
    return total


rules = {
    "play all turns": lambda h: False,
    "stop after the first win": lambda h: len(h) > 0 and h[-1] > 0,
    "stop after the first loss": lambda h: len(h) > 0 and h[-1] < 0,
    "stop when the total reaches 100 cents": lambda h: sum(h) >= 100,
    "stop at 200 cents of gain or loss": lambda h: abs(sum(h)) >= 200,
}
fair = ((100, F(1, 2)), (-100, F(1, 2)))
biased = ((150, F(1, 2)), (-100, F(1, 2)))
want_fair = {k: F(0) for k in rules}
want_biased = {
    "play all turns": F(150),
    "stop after the first win": F(1575, 32),
    "stop after the first loss": F(1575, 32),
    "stop when the total reaches 100 cents": F(575, 8),
    "stop at 200 cents of gain or loss": F(625, 8),
}
for name, rule in rules.items():
    check(f"L03 fair '{name}' expectation 0", expectation_by_sequences(fair, rule), want_fair[name])
    check(f"L03 biased '{name}' expectation", expectation_by_sequences(biased, rule), want_biased[name])

# Example 3.6 reroll game
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
check("L03 continuation 250", cont, F(250))
val = sum(max(F(100 * f), cont) for f in range(1, 7)) / 6
check("L03 reroll value 1150/3", val, F(1150, 3))
check("L03 gain 100/3", val - 350, F(100, 3))
best = max(
    sum((F(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6
    for bits in itertools.product((0, 1), repeat=6)
)
check("L03 best of 64 policies = 1150/3", best, F(1150, 3))
for c in (100, 1):
    v = sum(max(F(100 * f), F(350 - c)) for f in range(1, 7)) / 6 - 350
    check(f"L03 R2 gain at fee {c}", float(v), {100: 100 / 3, 1: 74.5}[c])
check("L03 R2 gain 100/3 exact", F(1150, 3) - 350, F(100, 3))
check("L03 M1 net 300", 100 * F(7, 2) - 50, F(300))
check("L03 M2 p=1/3", F(1, 3) * 200 - (1 - F(1, 3)) * 100, F(0))
check("L03 M3 two-stage 200", F(1, 2) * 100 + F(1, 2) * (-50 + 100 * F(7, 2)), F(200))
check("L03 E2 change -575/8", F(625, 8) - 150, F(-575, 8))
check("L03 E2 decimal -71.875", float(F(-575, 8)), -71.875)
# R1 look-ahead rule on the fair two-turn game
paths = [((100, 200)), ((100, 0)), ((-100, 0)), ((-100, -200))]
rule_total = [max(a, b) for a, b in paths]  # stop at the turn with the larger cumulative total
check("L03 R1 expectation 50", F(sum(rule_total), 4), F(50))
check("L03 Example 3.3 two dice E[X+Y]", F(sum(x + y for x in range(1, 7) for y in range(1, 7)), 36), F(7))
check("L03 Example 3.6 gap check: 2300/6", F(2300, 6), F(1150, 3))
print(f"SUMMARY checks={checks} fails={fails}")
