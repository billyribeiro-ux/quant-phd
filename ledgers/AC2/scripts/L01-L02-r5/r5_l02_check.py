"""Round-5 check of L02 twin numbers used in changed and unchanged prose (reads the twin, writes nothing)."""
import importlib.util
import sys

TWIN = "/tmp/verify-ac2r5-l12/tests/labs/AC2/lab-AC2-L02-1.py"
spec = importlib.util.spec_from_file_location("twin", TWIN)
twin = importlib.util.module_from_spec(spec)
sys.modules["twin"] = twin
spec.loader.exec_module(twin)

filer = twin.make_filer()
st = twin.standardize(filer)
for end, items in st.items():
    print(end, {k: items.get(k) for k in ("revenue", "cogs", "receivables", "current_assets", "current_liabilities", "long_term_debt", "total_assets")})

# DSO and gross margin and current ratio recomputed from the printed items, independent of twin helpers
for end, it in st.items():
    dso = it["receivables"] / it["revenue"] * 365
    gm = (it["revenue"] - it["cogs"]) / it["revenue"]
    cr = it["current_assets"] / it["current_liabilities"]
    print(f"{end} dso={dso:.4f} gm={gm:.4f} cr={cr:.4f}")
    assert abs(dso - twin.days_sales_outstanding(st, end)) < 1e-9
    assert abs(gm - twin.gross_margin(st, end)) < 1e-12
    assert abs(cr - twin.current_ratio(st, end)) < 1e-12
print("helpers agree with independent recomputation")

# Scale invariance of the three ratios with year-end balances and of gross margin (rule: ratios unchanged under x1000)
sc = twin.scaled(st, 1000.0)
for end in st:
    assert abs(twin.gross_margin(sc, end) - twin.gross_margin(st, end)) < 1e-12
    assert abs(twin.current_ratio(sc, end) - twin.current_ratio(st, end)) < 1e-12
print("scale invariance holds for gm and cr on every year")
