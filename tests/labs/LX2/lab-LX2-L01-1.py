"""LX2 lab L01: the registration-to-reporting model as a finite state machine, with the events the sections name.

Standard library only. No randomness, no network and no data. The lab is a model of the lesson's reading of
sections 5, 6 and 8 of the Securities Act of 1933 and sections 12, 13 and 15(d) of the Securities Exchange Act
of 1934. It is not a description of any issuer, filing or security.

A state is a pair (status, listing). The status is the status of the registration statement under the 1933 Act:
unregistered, filed, refused, effective or stop_order. The listing is whether the security is registered on a
national securities exchange under section 12 of the 1934 Act: not_listed or listed. The 1933 events apply
under either listing value, and the exchange events apply under every status, because the model does not
condition the listing on the status.

Assumption A1 (not read from the text): a security whose registration is under a stop order is still treated as
one whose 1933 registration has become effective, for the reporting-duty reading in duty_15d. The lab states
this as an assumption and does not claim the statute says it.

The lab enumerates every state and every transition, computes the states reachable from the start state, and
prints how many transitions leave the state set. It does not model the statutory timing (the twentieth day in
section 8(a) and the thirty days in section 12(d)), the exemptions, the prospectus requirement of section 5(b),
or the examinations and proceedings of section 8. Its printed flags are the lesson's reading, not a test the
Commission or a court applies.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Final

STATUSES: Final[tuple[str, ...]] = ("unregistered", "filed", "refused", "effective", "stop_order")
LISTINGS: Final[tuple[str, ...]] = ("not_listed", "listed")
START: Final[tuple[str, str]] = ("unregistered", "not_listed")

# (event, status before, status after, locator in the statute)
EVENTS_1933: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("file a registration statement", "unregistered", "filed", "section 6(a)"),
    ("refusal order before effectiveness", "filed", "refused", "section 8(b)"),
    ("amendment after a refusal order", "refused", "filed", "section 8(b)"),
    ("declare effective", "filed", "effective", "section 8(a)"),
    ("stop order", "effective", "stop_order", "section 8(d)"),
    ("stop order ceases after amendment", "stop_order", "effective", "section 8(d)"),
)

# (event, listing before, listing after, locator in the statute)
EVENTS_1934: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("register on a national securities exchange", "not_listed", "listed", "section 12(b) and 12(d)"),
    ("withdraw from listing and registration", "listed", "not_listed", "section 12(d)"),
)


@dataclass(frozen=True)
class Transition:
    """One event of the model: it moves the state from source to target, and cites its locator."""

    event: str
    source: tuple[str, str]
    target: tuple[str, str]
    locator: str


def make_transitions() -> list[Transition]:
    """Every transition of the model: the 1933 events under each listing, and the exchange events under each status."""
    out: list[Transition] = []
    for event, before, after, locator in EVENTS_1933:
        for listing in LISTINGS:
            out.append(Transition(event, (before, listing), (after, listing), locator))
    for event, before, after, locator in EVENTS_1934:
        for status in STATUSES:
            out.append(Transition(event, (status, before), (status, after), locator))
    return out


def reachable(start: tuple[str, str], transitions: list[Transition]) -> list[tuple[str, str]]:
    """The states reachable from start, in the order a breadth-first search first meets them."""
    order = [start]
    seen = {start}
    queue: deque[tuple[str, str]] = deque([start])
    while queue:
        current = queue.popleft()
        for t in transitions:
            if t.source == current and t.target not in seen:
                seen.add(t.target)
                order.append(t.target)
                queue.append(t.target)
    return order


def duty_13(state: tuple[str, str]) -> bool:
    """The lesson's reading of section 13(a): the duty applies to an issuer of a section 12 registered security."""
    return state[1] == "listed"


def duty_15d(state: tuple[str, str]) -> bool:
    """The lesson's reading of section 15(d)(1) under Assumption A1: the duty applies while the 1933 registration has
    become effective, which under A1 includes a stop order, and no section 12 registration is in force."""
    return state[0] in ("effective", "stop_order") and state[1] == "not_listed"


def offer_permitted(state: tuple[str, str]) -> bool:
    """The lesson's reading of section 5(c): an offer is permitted when the statement is filed or in effect, and not
    when it is refused or under a stop order."""
    return state[0] in ("filed", "effective")


def sale_permitted(state: tuple[str, str]) -> bool:
    """The lesson's reading of section 5(a): a sale through interstate means is unlawful unless a statement
    is in effect."""
    return state[0] == "effective"


def main() -> None:
    states = [(status, listing) for status in STATUSES for listing in LISTINGS]
    transitions = make_transitions()
    print(f"candidate states: {len(states)}, transitions: {len(transitions)}")
    leaving = [t.event for t in transitions if t.source not in states or t.target not in states]
    print(f"transitions that leave the state set: {len(leaving)}")
    reached = reachable(START, transitions)
    print(f"reachable from {START[0]}/{START[1]}: {len(reached)} of {len(states)}")
    print("state (status, listing)              reachable  s13(a)  s15(d)  offer  sale")
    for state in states:
        print(
            f"{state[0]:<13} {state[1]:<11}          {'yes' if state in reached else 'no':<10}"
            f"{'yes' if duty_13(state) else 'no':<8}{'yes' if duty_15d(state) else 'no':<8}"
            f"{'yes' if offer_permitted(state) else 'no':<7}{'yes' if sale_permitted(state) else 'no'}"
        )
    both = sum(duty_13(s) and duty_15d(s) for s in states)
    print(f"states where both reporting duties apply: {both}")
    sale_without_offer = sum(sale_permitted(s) and not offer_permitted(s) for s in states)
    print(f"states where a sale is permitted and an offer is not: {sale_without_offer}")
    print("transitions, with the locator each one cites:")
    for t in transitions:
        print(f"  {t.event}: {t.source[0]}/{t.source[1]} -> {t.target[0]}/{t.target[1]} [{t.locator}]")


main()
