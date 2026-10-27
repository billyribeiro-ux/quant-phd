"""Independent recomputation of the SIMULATED-filer numbers printed by Lab 1 and Lab 2 (AC2 L01/L02).

Reads the lab twins' generator (make_filer) by exec of their source without the trailing main() call,
then applies an independently written standardizer and DuPont (not the lab's code).
"""
import math, sys
from datetime import date

def load_generator(path):
    src = open(path, encoding="utf-8").read()
    assert src.rstrip().endswith("main()"), "expected trailing main()"
    src = src.rstrip()[: -len("main()")]
    ns = {}
    exec(compile(src, path, "exec"), ns)
    return ns["make_filer"]

ITEMS = {  # item: (tags in priority order, kind, unit)
 "revenue": (["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"], "flow", "USD"),
 "cogs": (["CostOfRevenue", "CostOfGoodsAndServicesSold"], "flow", "USD"),
 "sga": (["SellingGeneralAndAdministrativeExpense"], "flow", "USD"),
 "depreciation": (["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation"], "flow", "USD"),
 "operating_income": (["OperatingIncomeLoss"], "flow", "USD"),
 "net_income": (["NetIncomeLoss"], "flow", "USD"),
 "cfo": (["NetCashProvidedByUsedInOperatingActivities"], "flow", "USD"),
 "total_assets": (["Assets"], "inst", "USD"),
 "current_assets": (["AssetsCurrent"], "inst", "USD"),
 "cash": (["CashAndCashEquivalentsAtCarryingValue"], "inst", "USD"),
 "receivables": (["AccountsReceivableNetCurrent"], "inst", "USD"),
 "ppe": (["PropertyPlantAndEquipmentNet"], "inst", "USD"),
 "total_liabilities": (["Liabilities"], "inst", "USD"),
 "current_liabilities": (["LiabilitiesCurrent"], "inst", "USD"),
 "long_term_debt": (["LongTermDebtNoncurrent"], "inst", "USD"),
 "equity": (["StockholdersEquity"], "inst", "USD"),
 "shares_outstanding": (["CommonStockSharesOutstanding"], "inst", "shares"),
}

def d(s): return date.fromisoformat(s)

def std(facts, as_of=None):
    g = facts["facts"]["us-gaap"]
    cut = None if as_of is None else d(as_of)
    out = {}
    for item, (tags, kind, unit) in ITEMS.items():
        best_by_tag = {}
        for tag in tags:
            cands = {}
            for r in g.get(tag, {}).get("units", {}).get(unit, []):
                if not r["form"].startswith("10-K") or r.get("fp") != "FY":
                    continue
                if kind == "flow":
                    if "start" not in r: continue
                    dd = (d(r["end"]) - d(r["start"])).days
                    if not (350 <= dd <= 380): continue
                else:
                    if "start" in r: continue
                if cut and d(r["filed"]) > cut: continue
                cands.setdefault(r["end"], []).append(r)
            pick = {}
            for e, rs in cands.items():
                rs.sort(key=lambda r: (r["filed"], r.get("accn", "")), reverse=True)
                pick[e] = rs[0]
            best_by_tag[tag] = pick
        for tag in tags:
            for e, r in best_by_tag[tag].items():
                out.setdefault(e, {}).setdefault(item, (tag, r["val"]))
    # setdefault keeps the first tag in priority order that has the end (tags iterated in priority order)
    table = {}
    for e in sorted(out):
        table[e] = {k: v[1] for k, v in out[e].items()}
    return table

def prev_year(table, e):
    cands = [x for x in table if 350 <= (d(e) - d(x)).days <= 380]
    if not cands: raise ValueError("no previous year for " + e)
    return max(cands)

def avg(table, e, item):
    p = prev_year(table, e)
    return (table[e][item] + table[p][item]) / 2

def dupont(table, e):
    ni, rev = table[e]["net_income"], table[e]["revenue"]
    A, E = avg(table, e, "total_assets"), avg(table, e, "equity")
    nm, at, lev = ni / rev, rev / A, A / E
    roe = ni / E
    return dict(nm=nm, at=at, lev=lev, roe=roe, roa=ni / A, prod=nm * at * lev)

if __name__ == "__main__":
    make_filer = load_generator(sys.argv[1])
    filer = make_filer()
    t = std(filer)
    print("ends", list(t))
    for e in t:
        print(e, len(t[e]), round(t[e]["revenue"] / 1e6, 1), round(t[e]["net_income"] / 1e6, 1),
              round(t[e]["total_assets"] / 1e6, 1), round(t[e]["equity"] / 1e6, 1), "ltd" if "long_term_debt" in t[e] else "no-ltd")
    t23 = std(filer, "2023-06-30")
    t_all = std(filer)
    print("FY2022 rev as-of 2023-06-30 (M):", t23["2022-12-31"]["revenue"] / 1e6, " no cutoff:", t_all["2022-12-31"]["revenue"] / 1e6)
    print("period ends at 2023-06-30:", list(t23))
    print("restatement pct (exact):", 100 * (t_all["2022-12-31"]["revenue"] / t23["2022-12-31"]["revenue"] - 1))
    print("diff M:", (t_all["2022-12-31"]["revenue"] - t23["2022-12-31"]["revenue"]) / 1e6)
    print("2020 has ltd:", "long_term_debt" in t["2020-12-31"], " 2021 has ltd:", "long_term_debt" in t["2021-12-31"])
    print("2022 revenue tag check: values", {k: v for k, v in []})
    print("pre-2023-02-14 revenue absent for 2022:", "2022-12-31" not in std(filer, "2023-02-14"))
    print("2024 absent at 2025-01-31:", "2024-12-31" not in std(filer, "2025-01-31"), " present at 2025-02-15:", "2024-12-31" in std(filer, "2025-02-15"))
    print("--- Lab 2 numbers")
    for e in list(t)[1:]:
        x = dupont(t, e)
        print(e, round(x["nm"], 4), round(x["at"], 4), round(x["lev"], 4), round(x["roe"], 4), round(x["roa"], 4), abs(x["roe"] - x["prod"]) <= 1e-12 * x["roe"])
    for e in t:
        cur = t[e]["current_assets"] / t[e]["current_liabilities"]
        gm = (t[e]["revenue"] - t[e]["cogs"]) / t[e]["revenue"]
        dso = t[e]["receivables"] / t[e]["revenue"] * 365
        dta = t[e]["long_term_debt"] / t[e]["total_assets"] if "long_term_debt" in t[e] else None
        print(e, round(cur, 4), round(gm, 4), None if dta is None else round(dta, 4), round(dso, 2))
    y = "2022-12-31"
    ae = avg(t, y, "equity")
    print("avg equity 2022 (M):", round(ae / 1e6, 1), "roe avg", round(t[y]["net_income"] / ae, 4), "roe ye", round(t[y]["net_income"] / t[y]["equity"], 4))
    print("ROE gap %:", round(100 * ((t[y]["net_income"] / ae) / (t[y]["net_income"] / t[y]["equity"]) - 1), 2))
    print("as filed NM", round(t23[y]["net_income"] / t23[y]["revenue"], 4), "restated NM", round(t[y]["net_income"] / t[y]["revenue"], 4))
    print("as filed NM (cut 23-06-30 NI)", round(std(filer, "2023-06-30")[y]["net_income"] / t23[y]["revenue"], 4))
    mism = dupont(t, y)["nm"] * (t[y]["revenue"] / t[y]["total_assets"]) * dupont(t, y)["lev"]
    print("mismatch product", round(mism, 4))
    a, b = "2023-12-31", "2024-12-31"
    da, db = dupont(t, a), dupont(t, b)
    L = math.log(db["roe"] / da["roe"])
    print("log ROE change", round(L, 4))
    for f in ("nm", "at", "lev"):
        s = math.log(db[f] / da[f])
        print(f, round(s, 4), round(100 * s / L, 2))
    print("ROE 2021->2022, 2022->2023, 2023->2024 pct:", [round(100 * (dupont(t, n)["roe"] / dupont(t, p)["roe"] - 1), 2) for p, n in [("2021-12-31", "2022-12-31"), ("2022-12-31", "2023-12-31"), ("2023-12-31", "2024-12-31")]])
    print("DSO 2022 by hand", round(43.80 * 1131.9 / 1145.5, 2))
    print("growth ratio check 2(1+g)/(2+g) g=0.2:", round(2 * 1.2 / 2.2, 4))
    print("R2 check: (1.05/0.98)-1 =", round(1.05 / 0.98 - 1, 4), " bias", round(1.05 * 0.02 / 0.98, 5))
    print("M1 check NI 50 rev 500 A 800/700 E 300/260:", 50/500, 500/750, 750/280, 50/280, 50/750, 0.1*(500/750)*(750/280))
    print("M2 DSO 120/900*365, *360:", round(120/900*365, 2), 120/900*360, 365/360)
    print("M3 CR, GM:", 400/250, (1000-640)/1000)
