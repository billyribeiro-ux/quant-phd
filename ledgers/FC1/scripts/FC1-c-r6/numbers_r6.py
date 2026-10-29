from fractions import Fraction as F
y = F(400, 10000)
ev = [(1, 5000), (2, 5000), (3, 105000)]
pv = sum(F(a) / (1 + y) ** t for t, a in ev)
print("pv project p1", float(pv), f"{float(pv):.6f}", "exact", pv)
ev2 = [(1, 500), (2, 500), (3, 10500)]
pv2 = sum(F(a) / (1 + y) ** t for t, a in ev2)
print("rounding case exact", float(pv2), f"{float(pv2):.6f}", "terms", [float(F(a)/(1+y)**t) for t,a in ev2])
print("fixture B exact", float(F(10500)/F(95,100)), F(10500)/F(95,100), float(F(210000,19)))
print("fixture A", F(10500)/F(105,100))
print("ROUNDING via half-up", (pv2 + F(1,2)).__floor__())
print("tolerance 1e-6 * 102775 =", 1e-6*102775, " 1e-6*pv", 1e-6*float(pv))
