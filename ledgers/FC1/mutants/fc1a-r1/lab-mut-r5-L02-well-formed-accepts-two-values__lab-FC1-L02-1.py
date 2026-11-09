"""FC1 lab L02: a consistency check on a typed-in instrument register.

This is a consistency check on bookkeeping, not evidence about any market. The register below is typed in for the
lab. Each entry is given three classifications, one per axis: exposure (the economic risk its payoff depends on),
form (cash or derivative) and venue (exchange or over-the-counter). The venue assigned to an entry is an illustration
of the classification, not a statement about where that instrument trades. The checks test the register's own counts:
each entry has exactly one value on each axis, the counts on each axis reconcile to the number of entries, and a
deliberately malformed entry is rejected. No random numbers; standard library only; no network.
"""

from __future__ import annotations

from collections import Counter

EXPOSURES = ("equities", "rates", "credit", "fx", "commodities")
FORMS = ("cash", "derivative")
VENUES = ("exchange", "otc")
AXES: dict[str, tuple[str, ...]] = {"exposure": EXPOSURES, "form": FORMS, "venue": VENUES}

Entry = tuple[str, dict[str, tuple[str, ...]]]

REGISTER: list[Entry] = [
    ("share listed on an exchange", {"exposure": ("equities",), "form": ("cash",), "venue": ("exchange",)}),
    ("share sold in a private negotiated trade", {"exposure": ("equities",), "form": ("cash",), "venue": ("otc",)}),
    (
        "futures contract on an equity index",
        {"exposure": ("equities",), "form": ("derivative",), "venue": ("exchange",)},
    ),
    ("bond with a fixed coupon", {"exposure": ("rates",), "form": ("cash",), "venue": ("otc",)}),
    (
        "futures contract on a government bond",
        {"exposure": ("rates",), "form": ("derivative",), "venue": ("exchange",)},
    ),
    ("interest rate swap", {"exposure": ("rates",), "form": ("derivative",), "venue": ("otc",)}),
    ("corporate bond", {"exposure": ("credit",), "form": ("cash",), "venue": ("otc",)}),
    ("credit default swap", {"exposure": ("credit",), "form": ("derivative",), "venue": ("otc",)}),
    ("spot purchase of a currency", {"exposure": ("fx",), "form": ("cash",), "venue": ("otc",)}),
    ("forward contract on a currency", {"exposure": ("fx",), "form": ("derivative",), "venue": ("otc",)}),
    ("futures contract on crude oil", {"exposure": ("commodities",), "form": ("derivative",), "venue": ("exchange",)}),
    ("physical quantity of a metal", {"exposure": ("commodities",), "form": ("cash",), "venue": ("otc",)}),
]


def well_formed(entry: Entry) -> bool:
    """True when the entry has exactly one value on each axis and that value is an allowed one."""
    _, values = entry
    if set(values) != set(AXES):
        return False
    return all(len(values[axis]) >= 1 and values[axis][0] in allowed for axis, allowed in AXES.items())


def axis_counts(entries: list[Entry], axis: str) -> Counter[str]:
    """Count the entries carrying each value on one axis (an entry with two values counts under both)."""
    counts: Counter[str] = Counter()
    for _, values in entries:
        counts.update(values.get(axis, ()))
    return counts


def main() -> None:
    print("A. Each entry has exactly one value on each axis")
    results = [well_formed(entry) for entry in REGISTER]
    print(f"entries in the register: {len(REGISTER)}; well formed: {sum(results)}")
    print("every entry is well formed:", all(results))

    print()
    print("B. Counts on each axis reconcile to the number of entries")
    for axis, allowed in AXES.items():
        counts = axis_counts(REGISTER, axis)
        line = ", ".join(f"{value} {counts[value]}" for value in allowed)
        total = sum(counts[value] for value in allowed)
        print(f"{axis}: {line}; total {total}; reconciles: {total == len(REGISTER)}")

    print()
    print("C. The venue axis is separate from the form axis: exchange entries by form")
    exchange = [entry for entry in REGISTER if entry[1]["venue"] == ("exchange",)]
    by_form = Counter(entry[1]["form"][0] for entry in exchange)
    print(f"exchange entries: {len(exchange)}; cash {by_form['cash']}; derivative {by_form['derivative']}")
    exposures = sorted({entry[1]["exposure"][0] for entry in exchange})
    print(f"exposure classes with at least one exchange entry: {len(exposures)} ({', '.join(exposures)})")

    print()
    print("D. A malformed entry is rejected by the same check")
    malformed: Entry = (
        "entry with two exposures",
        {"exposure": ("rates", "credit"), "form": ("cash",), "venue": ("otc",)},
    )
    print("malformed entry rejected:", not well_formed(malformed))
    extended = [*REGISTER, malformed]
    total_with_malformed = sum(axis_counts(extended, "exposure").values())
    print(f"exposure total with the malformed entry added: {total_with_malformed} for {len(extended)} entries")
    print("the exposure total no longer reconciles to the entry count:", total_with_malformed != len(extended))


main()
