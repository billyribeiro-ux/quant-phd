"""Exact check of Proposition 3.1 (L04) with a FIXED quote (9990, 10010), L=10, p=1/2.

Hypothesis H1 fixes I_{t-1}=0 as a path event. The displayed conclusion conditions on v_t=v only.
This script computes, by exact enumeration over (fair value, inventory) states, the one-turn trade term
X = c_t + sigma_t v_t at turn t, and compares:
  (a) E[X | v_t = v]                    (the displayed conditioning)
  (b) E[X | v_t = v, I_{t-1} = 0]       (the conditioning H1 needs)
  (c) the closed form (1-p)h - p[(v-a)^+ + (b-v)^+]
"""

from __future__ import annotations

from fractions import Fraction
from collections import defaultdict

A = 10010
B = 9990
H = (A - B) // 2
L = 10
P_INFORMED = Fraction(1, 2)
P_UB = Fraction(1, 4)
P_US = Fraction(1, 4)
V0 = 10000
T = 11  # turn t of interest; the state before it is after t-1 = 10 full turns


def step_states(states: dict[tuple[int, int], Fraction]) -> dict[tuple[int, int], Fraction]:
    """One full turn (fair move, then arrival) on the (v_t, I_t) state law, with fills per A5."""
    out: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for (v_prev, inv), pr in states.items():
        for eps in (5, -5):
            v = v_prev + eps
            pe = pr / 2
            # uninformed buy by customer: maker sells, inventory -1, fill iff |inv-1| <= L
            if abs(inv - 1) <= L:
                out[(v, inv - 1)] += pe * P_UB
            else:
                out[(v, inv)] += pe * P_UB
            # uninformed sell by customer: maker buys, inventory +1
            if abs(inv + 1) <= L:
                out[(v, inv + 1)] += pe * P_US
            else:
                out[(v, inv)] += pe * P_US
            # informed: buys at ask if v > A, sells at bid if v < B, else no trade
            pi = pe * P_INFORMED
            if v > A:
                if abs(inv - 1) <= L:
                    out[(v, inv - 1)] += pi
                else:
                    out[(v, inv)] += pi
            elif v < B:
                if abs(inv + 1) <= L:
                    out[(v, inv + 1)] += pi
                else:
                    out[(v, inv)] += pi
            else:
                out[(v, inv)] += pi
    return dict(out)


def trade_term(v: int, inv: int) -> Fraction:
    """Expected c + sigma v given fair value v at turn t and inventory inv before turn t (fixed quote)."""
    total = Fraction(0)
    # uninformed buy: sigma=-1, c=A, fill iff |inv-1|<=L
    if abs(inv - 1) <= L:
        total += P_UB * (A - v)
    if abs(inv + 1) <= L:
        total += P_US * (v - B)
    if v > A and abs(inv - 1) <= L:
        total += P_INFORMED * (A - v)
    elif v < B and abs(inv + 1) <= L:
        total += P_INFORMED * (v - B)
    return total


def closed_form(v: int) -> Fraction:
    return (1 - P_INFORMED) * H - P_INFORMED * (max(v - A, 0) + max(B - v, 0))


def first_gap_turn() -> None:
    for t in range(2, 21):
        states: dict[tuple[int, int], Fraction] = {(V0, 0): Fraction(1)}
        for _ in range(t - 1):
            states = step_states(states)
        joint: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
        for (v_prev, inv), pr in states.items():
            for eps in (5, -5):
                joint[(v_prev + eps, inv)] += pr / 2
        gaps = []
        for v in sorted({vv for (vv, _) in joint}):
            pv = sum(p for (vv, _), p in joint.items() if vv == v)
            if pv == 0:
                continue
            ev = sum(p * trade_term(v, i) for (vv, i), p in joint.items() if vv == v) / pv
            if ev != closed_form(v):
                gaps.append(v)
        print(f"t={t:>2}: max |I_(t-1)| possible = {max(abs(i) for (_, i) in joint):>2}; v_t values with E[X|v] != closed form: {len(gaps)}")


def main() -> None:
    first_gap_turn()
    states: dict[tuple[int, int], Fraction] = {(V0, 0): Fraction(1)}
    for _ in range(T - 1):
        states = step_states(states)
    # now states are (v_{t-1}, I_{t-1}) in the step below; step once more to get (v_t, I_{t-1}) before the arrival
    # Build joint law of (v_t, I_{t-1}): fair move only.
    joint: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for (v_prev, inv), pr in states.items():
        for eps in (5, -5):
            joint[(v_prev + eps, inv)] += pr / 2
    total_prob = sum(joint.values())
    assert total_prob == 1, total_prob
    print(f"turn t = {T}; joint law of (v_t, I_(t-1)) after {T - 1} full turns; total probability {total_prob}")
    max_abs_inv = max(abs(i) for (_, i) in joint)
    print(f"largest |I_(t-1)| with positive probability: {max_abs_inv} (limit {L})")
    print(f"P(I_(t-1)=0) = {sum(p for (_, i), p in joint.items() if i == 0)}")
    print()
    print("v_t    closed form   E[X|v]        E[X|v,I=0]    E[X|v] - closed form")
    for v in (9975, 9985, 9995, 10005, 10015, 10025):
        pv = sum(p for (vv, _), p in joint.items() if vv == v)
        if pv == 0:
            print(v, "zero probability at this turn")
            continue
        ev = sum(p * trade_term(v, i) for (vv, i), p in joint.items() if vv == v) / pv
        p0 = joint.get((v, 0), Fraction(0))
        e0 = trade_term(v, 0)  # exact given I=0 and v
        cf = closed_form(v)
        print(f"{v}  {str(cf):>12}  {str(ev):>12}  {str(e0):>12}  {str(ev - cf):>12}  P(I=0,v)={p0 != 0}")


if __name__ == "__main__":
    main()


def fix_check() -> None:
    """Checks the candidate fixes: (i) conditioning on I_{t-1} = 0 and v_t = v; (ii) conditioning on |I_{t-1}| <= L-1."""
    states: dict[tuple[int, int], Fraction] = {(V0, 0): Fraction(1)}
    for _ in range(T - 1):
        states = step_states(states)
    joint: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for (v_prev, inv), pr in states.items():
        for eps in (5, -5):
            joint[(v_prev + eps, inv)] += pr / 2
    v = 9995
    p_v = sum(p for (vv, _), p in joint.items() if vv == v)
    num_all = sum(p * trade_term(v, i) for (vv, i), p in joint.items() if vv == v)
    p_lim = sum(p for (vv, i), p in joint.items() if vv == v and abs(i) <= L - 1)
    e_lim = sum(p * trade_term(v, i) for (vv, i), p in joint.items() if vv == v and abs(i) <= L - 1) / p_lim
    print()
    print(f"fix check at turn {T}, v_t = {v}:")
    print(f"  E[X | v_t=v]                 = {float(num_all / p_v):.12f}  (closed form {float(closed_form(v)):.12f})")
    print(f"  E[X | v_t=v, |I_(t-1)|<=L-1] = {float(e_lim):.12f}  (equal to closed form: {e_lim == closed_form(v)})")
    print(f"  E[X | v_t=v, I_(t-1)=0]      = {float(trade_term(v, 0)):.12f}  (equal to closed form: {trade_term(v, 0) == closed_form(v)})")
    print(f"  at I_(t-1)=10, v=10000: E[X] = {trade_term(10000, 10)} cents (closed form 5 cents)")


if __name__ == "__main__":
    fix_check()
