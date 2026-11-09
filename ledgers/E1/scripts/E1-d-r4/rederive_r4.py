"""Independent exact re-derivation for E1-d round 4 (does not import the reference or the grader)."""
from fractions import Fraction as F
import math, sys

def hu(x):
    return math.floor(x + F(1, 2))

def exact(structure, a, b, c):
    d = F(a - b * c)
    Q = {"monopoly": d / 2, "cournot": 2 * d / 3, "bertrand": d}[structure]
    fee = F(a) / b - Q / b          # inverse demand (a - Q)/b evaluated directly
    profit = (fee - c) * Q
    cs = Q * Q / (2 * b)
    w = F(a) * Q / b - F(Q * Q, 2 * b) - c * Q   # gross value minus cost
    dwl = (d - Q) ** 2 / (2 * b)
    return dict(volume=Q, fee=fee, profit=profit, cs=cs, welfare=w, dwl=dwl)

def printed(structure, a, b, c):
    e = exact(structure, a, b, c)
    return {k: hu(v) for k, v in e.items()}

# 1. Lab 1 / Lab 3 printed values
for a in (120, 121):
    for s in ("monopoly", "cournot", "bertrand"):
        print("lab3", a, s, printed(s, a, 1, 20))
print("lab1 exact cournot:", {k: str(v) for k, v in exact("cournot", 120, 1, 20).items()})
print("lab1 exact monopoly:", {k: str(v) for k, v in exact("monopoly", 120, 1, 20).items()})

# 2. Prop 5 ordering claim, brute force: whole a,b,c with d > 6b, printed orderings strict
bad = []
count = 0
for b in range(1, 7):
    for c in range(1, 25):
        for d in range(6 * b + 1, 6 * b + 260):
            a = b * c + d
            count += 1
            P = {s: printed(s, a, b, c) for s in ("monopoly", "cournot", "bertrand")}
            ok = (P["monopoly"]["volume"] < P["cournot"]["volume"] < P["bertrand"]["volume"]
                  and P["monopoly"]["fee"] > P["cournot"]["fee"] > c
                  and P["monopoly"]["dwl"] > P["cournot"]["dwl"] > P["bertrand"]["dwl"]
                  and P["monopoly"]["welfare"] < P["cournot"]["welfare"] < P["bertrand"]["welfare"]
                  and P["monopoly"]["profit"] > P["cournot"]["profit"] > P["bertrand"]["profit"])
            if not ok:
                bad.append((a, b, c))
print("prop5 cases", count, "violations", len(bad), bad[:5])

# 3. Boundary: is d > 6b needed? find smallest-d violations for small b
viol_small = []
for b in range(1, 4):
    for c in range(1, 15):
        for d in range(1, 6 * b + 3):
            a = b * c + d
            P = {s: printed(s, a, b, c) for s in ("monopoly", "cournot", "bertrand")}
            if not (P["monopoly"]["volume"] < P["cournot"]["volume"] < P["bertrand"]["volume"]):
                viol_small.append((a, b, c, "vol"))
print("d<=6b volume-order violations (informational):", len(viol_small), viol_small[:4])

# 4. Exact differences claimed in Proposition 5 proof and exemplars (reference case)
e = {s: exact(s, 120, 1, 20) for s in ("monopoly", "cournot", "bertrand")}
print("profit diff mono-cournot exact:", e["monopoly"]["profit"] - e["cournot"]["profit"], "= 2500/9?", e["monopoly"]["profit"] - e["cournot"]["profit"] == F(2500, 9))
print("d^2/(36b) for a=120:", F(100 * 100, 36))
print("fee diff mono-cournot:", e["monopoly"]["fee"] - e["cournot"]["fee"])
print("volume diffs:", e["cournot"]["volume"] - e["monopoly"]["volume"], e["bertrand"]["volume"] - e["cournot"]["volume"])
print("welfare diffs:", e["cournot"]["welfare"] - e["monopoly"]["welfare"], e["bertrand"]["welfare"] - e["cournot"]["welfare"])
print("CS cournot:", e["cournot"]["cs"], "DWL cournot:", e["cournot"]["dwl"])

# 5. Large exact input in grader comment
a = 15000000000000002
print("cournot volume a=1.5e16+2 b=c=1:", 2 * F(a - 1, 3), "=", float(2 * F(a - 1, 3)) if False else "", hu(2 * F(a - 1, 3)), 10**16 + 1)

# 6. Prop 2 iteration error and Lab 2 claim
q = F(0); d = F(100)
for k in range(60):
    q = (d - q) / 2
print("lab2 |q60 - d/3| =", abs(q - d / 3), "< 1e-12:", abs(q - d / 3) < F(1, 10**12), " d/(3*2^60)=", d / (3 * 2**60), float(d / (3 * 2**60)))

# 7. Lab 2 welfare expression equals consumer+profit form
Q = 2 * d / 3
print("lab2 welfare exact", (120 * Q - Q * Q / 2) / 1 - 20 * Q, "printed", hu((120 * Q - Q * Q / 2) / 1 - 20 * Q))

# 8. Exemplar B numbers
print("exemplarB DWL cournot", exact("cournot",120,1,20)["dwl"], hu(exact("cournot",120,1,20)["dwl"]))
print("exemplarB tie a=121 fee/vol", exact("monopoly",121,1,20)["fee"], exact("monopoly",121,1,20)["volume"])
