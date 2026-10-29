from fractions import Fraction
def step(h):  # R3 step table, 0 hours costs 0
    if h == 0: return 0
    return 4000 * -(-h // 400)
err = {h: abs(step(h) - 10 * h) for h in range(0, 1201)}
m = max(err.values())
print("max abs error", m, "at", [h for h in err if err[h] == m])
print("share of 4000 step", Fraction(m, 4000), float(Fraction(m, 4000)) * 100)
# DOL and volume check for L02 lab inputs
mg, F = 1350, 120000
print("breakeven", Fraction(F, mg), "ceil", -(-F // mg))
print("OI 2000 vs 2001 cents", 1350*2000 - F, 1350*2001 - F - 2700000)
print("loss runs by formula: 0..88 and 2001..2088 neg, 89..2000 pos, 2089 pos")
print("OI(88)", 1350*88 - F, "OI(89)", 1350*89 - F, "OI(2088)", 1350*2088 - F - 2700000, "OI(2089)", 1350*2089 - F - 2700000)
print("R3 weighted margins", (10 + 30) / 2, "BE 60000/10", 60000 // 10, "60000/20", 60000 // 20)
