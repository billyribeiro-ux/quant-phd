"""Lab CR4-project-2: Project Rung 2 Completion Problem Solution Twin.

Implements the core priority allocation and fulcrum detection algorithm.
The completion problem on project.html blanks out the inner allocation and fulcrum checks.
"""

from __future__ import annotations

from typing import NamedTuple


class Tranche(NamedTuple):
    name: str
    claim: float


def allocate_waterfall_step(
    tranches: list[Tranche],
    ev: float,
) -> tuple[list[dict[str, float | str]], str]:
    """Allocate EV down seniority tranches and return allocations and fulcrum name."""
    rem = float(ev)
    allocations: list[dict[str, float | str]] = []
    fulcrum_name = "None"
    fulcrum_found = False
    total_debt = sum(t.claim for t in tranches)

    for t in tranches:
        claim = t.claim
        alloc = min(rem, claim)
        rem -= alloc
        rec_pct = alloc / claim if claim > 0 else 0.0

        is_part = 0.0 < alloc < claim
        is_bound = abs(alloc - claim) < 1e-6 and abs(rem) < 1e-6
        if not fulcrum_found and ev < total_debt and claim > 0 and (is_part or is_bound):
            fulcrum_name = t.name
            fulcrum_found = True

        allocations.append(
            {
                "name": t.name,
                "claim": claim,
                "allocated": round(alloc, 2),
                "recovery_pct": round(rec_pct, 4),
            }
        )

    return allocations, fulcrum_name


def main() -> None:
    tranches = [
        Tranche("1st Lien Debt", 100.0),
        Tranche("2nd Lien Debt", 50.0),
        Tranche("Unsecured Debt", 60.0),
        Tranche("Subordinated Debt", 40.0),
    ]
    ev = 180.0

    allocs, fulcrum = allocate_waterfall_step(tranches, ev)

    print("Rung 2 Waterfall Completion Verification (EV = 180.0):")
    print("Tranche Name       | Claim ($M) | Allocated ($M) | Recovery (%)")
    print("-" * 62)
    for a in allocs:
        r_pct = float(a["recovery_pct"]) * 100.0
        c_val = float(a["claim"])
        al_val = float(a["allocated"])
        n_val = str(a["name"])
        print(f"{n_val:18} |    {c_val:5.1f}   |      {al_val:5.1f}     |    {r_pct:5.1f}%")

    print(f"\nIdentified Fulcrum Tranche: {fulcrum}")

    # Assertions
    assert allocs[0]["allocated"] == 100.0
    assert allocs[1]["allocated"] == 50.0
    assert allocs[2]["allocated"] == 30.0
    assert allocs[3]["allocated"] == 0.0
    assert fulcrum == "Unsecured Debt"
    assert sum(float(a["allocated"]) for a in allocs) == ev
    print("Verification succeeded: Priority strictly maintained and fulcrum identified.")


main()
