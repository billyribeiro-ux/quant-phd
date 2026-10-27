"""Round-2 independent recomputation for AC2 L03 with exact fractions.

Loads the twin's make_filer/standardize (the simulated data), re-derives every printed number and
every proposition/algebra claim with fractions.Fraction and with random exact states.
"""
import contextlib
import io
import random
import runpy
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(root / "tests/labs/AC2/lab-AC2-L03-1.py"), run_name="twin")
standardize = g["standardize"]
filer = g["make_filer"]()
st = standardize(filer)
fr = {e: {k: F(v) for k, v in row.items()} for e, row in st.items()}
ends = list(fr)

def ic(e):
    return fr[e]["equity"] + fr[e]["long_term_debt"] - fr[e]["cash"]

def roic(e, tau, prev):
    oi = fr[e]["operating_income"] * (1 - tau)
    return oi / ((ic(e) + ic(prev)) / 2)

print("period ends:", ends)
for e in ends:
    print(e, "IC", float(ic(e)) if "long_term_debt" in fr[e] else "absent", "OI", fr[e]["operating_income"], "NI", fr[e]["net_income"])
prev = {"2022-12-31": "2021-12-31", "2023-12-31": "2022-12-31", "2024-12-31": "2023-12-31"}
rates = [F(0), F(15, 100), F(21, 100), F(25, 100), F(30, 100)]
print("ROIC table (exact -> 4dp):")
for e in ("2022-12-31", "2023-12-31", "2024-12-31"):
    row = [roic(e, t, prev[e]) for t in rates]
    print(e, ["%.4f" % float(x) for x in row])
    dev = max(abs(roic(e, t, prev[e]) - roic(e, 0, prev[e]) * (1 - t)) / abs(roic(e, 0, prev[e])) for t in rates)
    print("  max relative deviation from ROIC(0)(1-t) (exact):", dev)

e = "2023-12-31"
p = "2022-12-31"
avg = (ic(e) + ic(p)) / 2
print("FY2023 avg IC", float(avg), "=", float(avg) / 1e6, "USD m")
print("FY2023 OI*0.75/avg", float(fr[e]["operating_income"] * F(3, 4) / avg), "year-end", float(fr[e]["operating_income"] * F(3, 4) / ic(e)))
print("ye/avg gap %", float((ic(e)/avg - 1)*100))
# cash not netted
def ic_nc(x):
    return x["equity"] + x["long_term_debt"]
avg_nc = (ic_nc(fr[e]) + ic_nc(fr[p])) / 2
r_nc = fr[e]["operating_income"] * F(3, 4) / avg_nc
r_net = roic(e, F(25, 100), p)
print("cash netted", "%.6f" % float(r_net), "not netted", "%.6f" % float(r_nc), "netted is higher by %.4f%%" % float((r_net / r_nc - 1) * 100))
# hypothetical 50m short-term debt
h = F(50_000_000)
avg_h = (ic(e) + h + ic(p) + h) / 2
print("with 50m STD: ROIC 25%", "%.6f" % float(fr[e]["operating_income"] * F(3, 4) / avg_h))
# implied rate
for x in ("2020-12-31", "2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"):
    print("implied", x, float(1 - fr[x]["net_income"] / fr[x]["operating_income"]))
# E1 decomposition
e24, p24 = "2024-12-31", "2023-12-31"
avg24 = (ic(e24) + ic(p24)) / 2
print("E1 avg IC 2024", float(avg24), "2023 avg", float(avg))
print("E1 nopat change", float(fr[e24]["operating_income"] * F(3,4) / (fr[e]["operating_income"] * F(3,4)) - 1))
print("E1 NOPAT 2024 at 25%", float(fr[e24]["operating_income"]*F(3,4))/1e6)
print("E1 avg IC change", float(avg24 / avg - 1))
print("E1 ROIC ratio exact", float(roic(e24, F(25,100), p24) / roic(e, F(25,100), p)), "0.0974/0.1349-1 ->", float(roic(e24, F(25,100), p24)/roic(e, F(25,100), p) - 1))
print("E1 ratio (1+dN)/(1+dIC)", float((fr[e24]["operating_income"]/fr[e]["operating_income"])/(avg24/avg)))
r2024 = roic(e24, 0, p24)
print("E2 2024 ROIC at 0 tax", float(r2024), "tau for 10%:", float(1 - F(1,10)/r2024))
print("E2 check 0.1 threshold 0.2301 =", float(1 - F(1,10)/F("0.1299")))
# E3 growth
for a, b in (("2021-12-31", "2022-12-31"), ("2022-12-31", "2023-12-31"), ("2023-12-31", "2024-12-31")):
    print("E3 growth into", b, float(ic(b)/ic(a) - 1))
print("E3 IC values", [float(ic(x)) for x in ends[1:]])
