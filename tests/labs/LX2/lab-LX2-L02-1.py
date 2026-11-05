"""LX2 lab L02: a rule-based classifier for eight insider-trading fact patterns, with the citation for each decision.

HYPOTHETICAL. The eight patterns are authored for this lab. None describes a real person, firm, security, filing or
court case, and nothing on the page says that a pattern happened.

Standard library only. No randomness, no network and no data. The classifier applies, in order, the elements that the
lesson states from two admitted opinions: Dirks v. SEC (key gpo1983dirks) and United States v. O'Hagan (key
gpo1997united). For each pattern it stops at the first element the pattern does not state, and reports that element
with the registry key and the printed page it rests on. A pattern that states every element of a branch fires it.

The three branches and the elements each one checks, in order:
  classical (role issuer_insider): material information; nonpublic information; a trade (the classifier does not test
    that the security is the issuer's); no public disclosure before the trade.
  tippee (role tippee): material and nonpublic information from an insider; a personal benefit to the tipper; the
    tippee traded; the tippee knew or should have known of the breach.
  misappropriation (role outsider): confidential information; a duty owed to its source; the information was used to
    trade; the source was not told of the trade before it was made.
A pattern with role outsider and no duty owed to its source fails the duty check, and no branch fires.

Materiality, confidentiality, benefit, knowledge and disclosure are facts that each pattern states. The classifier
reads them and does not assess them. It does not assess scienter, which the lesson treats as a separate element. A
fired branch means that the stated facts contain every element of the branch under the rules coded here. It does not
say how a court would rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

KEY_DIRKS: Final[str] = "gpo1983dirks"
KEY_O_HAGAN: Final[str] = "gpo1997united"
PERSONAL_BENEFITS: Final[dict[str, str]] = {
    "pecuniary": "p. 663",
    "reputational": "p. 663",
    "gift_to_relative_or_friend": "p. 664",
}
NO_BENEFIT_LOCATOR: Final[str] = "p. 662"
BRANCH_RULE: Final[dict[str, tuple[str, str]]] = {
    "classical": (KEY_O_HAGAN, "pp. 651-652"),
    "tippee": (KEY_DIRKS, "p. 660"),
    "misappropriation": (KEY_O_HAGAN, "p. 652"),
}


@dataclass(frozen=True)
class Pattern:
    """One HYPOTHETICAL fact pattern. Every flag is a fact the pattern states; the classifier does not assess it."""

    label: str
    role: str  # issuer_insider, tippee or outsider
    facts: str
    material: bool
    nonpublic: bool
    confidential: bool
    duty_to_source: bool
    traded: bool
    public_before_trade: bool
    source_told_of_trade: bool
    tipper_benefit: str  # pecuniary, reputational, gift_to_relative_or_friend, none or not_applicable
    knew_or_should_have_known: bool


@dataclass(frozen=True)
class Check:
    """One element of a branch: whether the pattern states it, and the key and printed page it rests on."""

    element: str
    passed: bool
    key: str
    locator: str


@dataclass(frozen=True)
class Decision:
    """The branch a pattern was tested against, whether it fired, and the element that decided the outcome."""

    label: str
    branch: str
    fired: bool
    element: str
    key: str
    locator: str


PATTERNS: Final[tuple[Pattern, ...]] = (
    Pattern(
        label="P1",
        role="issuer_insider",
        facts=(
            "A director of the issuer learns of an unannounced acquisition agreement and buys shares before "
            "any announcement."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="not_applicable",
        knew_or_should_have_known=False,
    ),
    Pattern(
        label="P2",
        role="tippee",
        facts=(
            "A senior officer of the issuer tells a friend about a pending product recall. The officer "
            "receives nothing, and the friend trades."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="none",
        knew_or_should_have_known=True,
    ),
    Pattern(
        label="P3",
        role="tippee",
        facts=(
            "A mid-level employee of the issuer tells a fund manager about a pending merger for a cash "
            "payment. The manager trades."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="pecuniary",
        knew_or_should_have_known=True,
    ),
    Pattern(
        label="P4",
        role="tippee",
        facts="A corporate lawyer gives her brother-in-law advance word of a tender offer, with no payment. He trades.",
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="gift_to_relative_or_friend",
        knew_or_should_have_known=True,
    ),
    Pattern(
        label="P5",
        role="tippee",
        facts=(
            "An officer of the issuer gives a fund manager a tip for a cash payment. The manager has no "
            "reason to know of the payment, and trades."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="pecuniary",
        knew_or_should_have_known=False,
    ),
    Pattern(
        label="P6",
        role="outsider",
        facts=(
            "An associate at an accounting firm reads a client's confidential file on a planned acquisition "
            "of a target company. He buys the target's shares before the announcement and does not tell the "
            "client."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=True,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="not_applicable",
        knew_or_should_have_known=False,
    ),
    Pattern(
        label="P7",
        role="outsider",
        facts=(
            "The same associate tells the client in writing that he plans to buy the target's shares, and "
            "then buys them."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=True,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=True,
        tipper_benefit="not_applicable",
        knew_or_should_have_known=False,
    ),
    Pattern(
        label="P8",
        role="outsider",
        facts=(
            "A stranger overhears two executives discuss a planned acquisition on a train, has no "
            "relationship with them, and buys the target's shares."
        ),
        material=True,
        nonpublic=True,
        confidential=True,
        duty_to_source=False,
        traded=True,
        public_before_trade=False,
        source_told_of_trade=False,
        tipper_benefit="not_applicable",
        knew_or_should_have_known=False,
    ),
)


def branch_checks(p: Pattern) -> tuple[str, tuple[Check, ...]]:
    """The branch a pattern is tested against, and its elements in the order the classifier checks them."""
    if p.role == "issuer_insider":
        return "classical", (
            Check("material information", p.material, KEY_O_HAGAN, "pp. 651-652"),
            Check("nonpublic information", p.nonpublic, KEY_O_HAGAN, "pp. 651-652"),
            Check("a trade", p.traded, KEY_O_HAGAN, "pp. 651-652"),
            Check("no public disclosure before the trade", not p.public_before_trade, KEY_DIRKS, "p. 654"),
        )
    if p.role == "tippee":
        benefit_ok = p.tipper_benefit in PERSONAL_BENEFITS
        benefit_locator = PERSONAL_BENEFITS[p.tipper_benefit] if benefit_ok else NO_BENEFIT_LOCATOR
        return "tippee", (
            Check("material nonpublic information from an insider", p.material and p.nonpublic, KEY_DIRKS, "p. 654"),
            Check(f"tipper's personal benefit ({p.tipper_benefit})", benefit_ok, KEY_DIRKS, benefit_locator),
            Check("tippee traded", p.traded, KEY_DIRKS, "p. 660"),
            Check("tippee knew or should have known of the breach", p.knew_or_should_have_known, KEY_DIRKS, "p. 660"),
        )
    if p.role == "outsider":
        return "misappropriation", (
            Check("confidential information", p.confidential, KEY_O_HAGAN, "p. 652"),
            Check("duty owed to the source of the information", p.duty_to_source, KEY_O_HAGAN, "p. 652"),
            Check("information used to trade", p.traded, KEY_O_HAGAN, "p. 656"),
            Check("source not told of the trade before it was made", not p.source_told_of_trade, KEY_O_HAGAN, "p. 655"),
        )
    raise ValueError(f"{p.label}: unknown role {p.role!r}")


def classify(p: Pattern) -> Decision:
    """The first element the pattern does not state decides the outcome; if none fails, the branch fires."""
    branch, checks = branch_checks(p)
    for check in checks:
        if not check.passed:
            return Decision(p.label, branch, False, f"fails: {check.element}", check.key, check.locator)
    key, locator = BRANCH_RULE[branch]
    return Decision(p.label, branch, True, "all elements stated", key, locator)


def main() -> None:
    """Print each pattern's facts, then the decision for each one, then the two lists of labels."""
    print("LX2 lab L02: insider-trading fact-pattern classifier. HYPOTHETICAL patterns; rules as coded in this lab.")
    print()
    for p in PATTERNS:
        print(f"{p.label}: {p.facts}")
    decisions = [classify(p) for p in PATTERNS]
    print()
    print(f"{'pattern':<9}{'branch':<19}{'result':<11}{'deciding element':<60}{'key':<15}locator")
    for d in decisions:
        result = "fired" if d.fired else "not fired"
        print(f"{d.label:<9}{d.branch:<19}{result:<11}{d.element:<60}{d.key:<15}{d.locator}")
    fired = [d.label for d in decisions if d.fired]
    not_fired = [d.label for d in decisions if not d.fired]
    print()
    print(f"fired: {', '.join(fired)} ({len(fired)} of {len(decisions)})")
    print(f"not fired: {', '.join(not_fired)} ({len(not_fired)} of {len(decisions)})")
    print("Read as stated, not assessed: materiality, confidentiality, benefit, knowledge and disclosure.")
    print("Scienter is not checked.")


main()
