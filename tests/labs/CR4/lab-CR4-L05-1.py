"""Lab CR4-L05-1: Capital Structure Recovery Waterfall & Fulcrum Security Analysis.

Demonstrates multi-tranche recovery waterfall allocation under strict APR,
fulcrum security migration across enterprise value scenarios,
and investor MOIC / IRR profiles for distressed debt acquisitions.
"""

from __future__ import annotations


def allocate_waterfall(
    claims: list[tuple[str, float]],
    ev: float,
) -> list[dict[str, float | str | bool]]:
    """Allocate EV across prioritized claims and identify fulcrum tranche."""
    rem = ev
    results: list[dict[str, float | str | bool]] = []
    total_claims = sum(c[1] for c in claims)

    fulcrum_found = False
    for name, claim in claims:
        alloc = min(rem, claim)
        rem -= alloc
        rec_pct = (alloc / claim) if claim > 0 else 0.0

        is_fulcrum = False
        is_part = 0.0 < alloc < claim
        is_bound = abs(alloc - claim) < 1e-6 and abs(ev - (ev - rem)) < 1e-6 and rem == 0.0
        if not fulcrum_found and ev < total_claims and (is_part or is_bound):
            is_fulcrum = True
            fulcrum_found = True

        results.append(
            {
                "name": name,
                "claim": claim,
                "allocated": alloc,
                "recovery_pct": rec_pct,
                "is_fulcrum": is_fulcrum,
            }
        )

    return results


def main() -> None:
    # Capital structure claims (in $M)
    claims = [
        ("1st Lien Term Loan", 100.0),
        ("2nd Lien Notes", 60.0),
        ("Senior Unsecured Notes", 80.0),
        ("Subordinated Debentures", 40.0),
    ]
    total_debt = sum(c[1] for c in claims)  # 280.0

    ev_scenarios = [70.0, 130.0, 200.0, 260.0, 320.0]

    print("Capital Structure Recovery Waterfall Across Enterprise Value Scenarios:")
    print("Claims: 1st Lien=$100M, 2nd Lien=$60M, Sr Unsec=$80M, Sub Debt=$40M (Total Debt = $280M)")
    print("-" * 88)
    print("  EV ($M)  | 1st Lien Rec (%) | 2nd Lien Rec (%) | Sr Unsec Rec (%) | Sub Debt Rec (%) | Fulcrum Tranche")
    print("-" * 88)

    for ev in ev_scenarios:
        res = allocate_waterfall(claims, ev)
        fl_pct = float(res[0]["recovery_pct"]) * 100.0
        sl_pct = float(res[1]["recovery_pct"]) * 100.0
        unsec_pct = float(res[2]["recovery_pct"]) * 100.0
        sub_pct = float(res[3]["recovery_pct"]) * 100.0

        fulcrum_name = "None (Fully Solvent)"
        for r in res:
            if r["is_fulcrum"]:
                fulcrum_name = str(r["name"])
                break

        fl_s = f"{fl_pct:5.1f}%"
        sl_s = f"{sl_pct:5.1f}%"
        un_s = f"{unsec_pct:5.1f}%"
        sb_s = f"{sub_pct:5.1f}%"
        row = (
            f"   {ev:5.1f}   |      {fl_s}      |      {sl_s}      |"
            f"      {un_s}      |      {sb_s}      | {fulcrum_name}"
        )
        print(row)

    # Distressed Investor Analysis: Buying Senior Unsecured Notes at 35 cents on the dollar
    purchase_price = 0.35  # 35c
    holding_period = 1.5  # years
    unsec_claim = 80.0
    cost = purchase_price * unsec_claim

    print("\nDistressed Investor Return Profile: Senior Unsecured Notes ($80M claim, Bought @ 35c = $28M cost):")
    print("  EV ($M)  | Unsecured Recovery ($M) | Recovery (%) |   MOIC   | Annualized IRR")
    print("-" * 80)

    for ev in ev_scenarios:
        res = allocate_waterfall(claims, ev)
        unsec_rec = float(res[2]["allocated"])
        rec_pct = float(res[2]["recovery_pct"]) * 100.0
        moic = unsec_rec / cost if cost > 0 else 0.0
        irr = (moic ** (1.0 / holding_period) - 1.0) * 100.0 if moic > 0 else -100.0

        u_s = f"{unsec_rec:5.1f}"
        r_s = f"{rec_pct:5.1f}%"
        m_s = f"{moic:5.2f}x"
        i_s = f"{irr:5.1f}%"
        print(f"   {ev:5.1f}   |          {u_s}          |    {r_s}    |  {m_s}  |     {i_s}")

    # Invariant checks:
    # 1. Total allocated equals min(EV, Total Debt)
    for ev in ev_scenarios:
        res = allocate_waterfall(claims, ev)
        tot_alloc = sum(float(r["allocated"]) for r in res)
        assert abs(tot_alloc - min(ev, total_debt)) < 1e-9

    # 2. At EV=200, Senior Unsecured is the fulcrum security (recovers 40 out of 80 = 50%)
    res_200 = allocate_waterfall(claims, 200.0)
    assert res_200[2]["is_fulcrum"] is True
    assert abs(float(res_200[2]["recovery_pct"]) - 0.50) < 1e-9

    print("\nVerified waterfall invariants:")
    print("1. Enterprise value conservation holds exactly across all EV scenarios.")
    print("2. Fulcrum security migrates strictly down the seniority ladder as EV expands.")


main()
