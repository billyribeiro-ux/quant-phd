"""Round-15 verifier: recompute every number in the changed and slice prose of L05-L08 from first principles."""
from fractions import Fraction as F
import math
from decimal import Decimal, getcontext

getcontext().prec = 50

def omega(p):
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))

def omega_gen(p, eta=0.5):
    return p**eta / (p**eta + (1 - p)**eta) ** (1 / eta)

print("omega(0.3)", repr(omega(0.3)), "omega(0.6)", repr(omega(0.6)), "omega(0.4)", repr(omega(0.4)))
print("omega(0.5)", repr(omega(0.5)), "1/(2sqrt2)", repr(1 / (2 * math.sqrt(2))))
print("omega(0.01)", repr(omega(0.01)), "omega(0.99)", repr(omega(0.99)))
print("omega(0.25)", repr(omega(0.25)), "2-sqrt3", repr(2 - math.sqrt(3)), "1/(2+sqrt3)", repr(1/(2+math.sqrt(3))))
print("sum A weights", repr(omega(0.4) + 2 * omega(0.3)))
print("ratio w(.3)/w(.6)", repr(omega(0.3) / omega(0.6)), "threshold a=1", 2 / 3, "a=1/2", 1 / (1 + 2 ** -0.5))
print("G(A) alpha=1", 150 * omega(0.3), "G(B)", 100 * omega(0.6), "diff", 150 * omega(0.3) - 100 * omega(0.6))
print("G(A) alpha=.5", 0.3 and omega(0.3) * (50**0.5 + 100**0.5), "G(B)", omega(0.6) * 100**0.5)
# 40-digit values
def om_dec(p):
    p = Decimal(p)
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())
gA = 150 * om_dec("0.3")
gB = 100 * om_dec("0.6")
print("dec G(A)", gA, "dec G(B)", gB, "dec diff", gA - gB)
print("dec w(0.01)", om_dec("0.01"), "dec w(0.99)", om_dec("0.99"))
print("dec ratio", om_dec("0.3") / om_dec("0.6"))
# Remark 1.6 & misconception numbers
w001 = float(om_dec("0.01")); w099 = float(om_dec("0.99"))
print("weighted L", w001 * 100 + w099 * 50, "EV", 0.01 * 100 + 0.99 * 50)
print("over", (w001 - 0.01) * 100, "under", (0.99 - w099) * 50, "net", (w001 - 0.01) * 100 - (0.99 - w099) * 50)
# crossing on grid
grid = [i / 1000 for i in range(1001)]
above = [omega(p) > p for p in grid[1:-1]]
ch = sum(1 for a, b in zip(above, above[1:]) if a != b)
last = max(p for p in grid[1:-1] if omega(p) > p)
print("sign changes", ch, "last above", last, "w(0.279)-0.279", omega(0.279) - 0.279)
# closed form vs general gap, eta=1/2
gap = max(abs(omega_gen(p) - omega(p)) for p in grid[1:-1])
print("closed vs general max gap (eta=.5)", gap)
# eta=1 gap: closed form vs p
gap1 = max(((abs(omega(p) - p), p) for p in grid[1:-1]))
print("closed form vs p (eta=1 general) max gap", gap1)
# Example 2.1 lottery checks
print("EU identity sums", 0.6*100, 0.3*50+0.3*100)
# L07 E2 prints
print("printed diff", round(42.8686, 4) - round(39.1251, 4))
# L05 numbers
print("CE games", 1/((1+0.25)/2), 1/((0.5+1/3)/2))
print("CE g=3", (32/17) ** 0.5, "CE g=0.5", ((1+2)/2) ** 2)
print("L06 sqrt(5/3)", math.sqrt(5/3), "lam_R", 0.5*math.sqrt(2))
print("L06 W(2) alpha=.5", 0.5*math.sqrt(1000) - 0.5*2*math.sqrt(600))
print("L06 Example 2.3", 0.5*1000-0.5*600, 0.5*1000-0.5*1.5*600, 0.5*1000-0.5*2*600)
print("L05 V0 sure", 1/(0.1/2 + 0.9*(5/8)), 80/49, "V0 (4,4)", 4.0, "V0(1,10)", (0.5*1**-0.5 + 0.5*10**-0.5)**-2 if False else None)
