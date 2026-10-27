# Round 9: witnesses for the L02q3 option, canon line 666 and card AC2-c024.
# Identity per year: total assets A = liabilities L + equity E (articulation). Factor = avg A / avg E over two year ends.
def avg(x, y): return (x + y) / 2
def factor(a0, e0, a1, e1): return avg(a0, a1) / avg(e0, e1)
# Check 1: A = L + E gives avgA/avgE = 1 + avgL/avgE (exact).
L0, E0, L1, E1 = 300.0, 100.0, 340.0, 100.0
A0, A1 = L0 + E0, L1 + E1
assert abs(factor(A0, E0, A1, E1) - (1 + avg(L0, L1) / avg(E0, E1))) < 1e-12
print("identity check ok")
# Check 2: equity unchanged (E0 = E1 = 100); a payables increase of 40 in year 1 only raises the factor.
base = factor(400.0, 100.0, 400.0, 100.0)
pay = factor(400.0, 100.0, 440.0, 100.0)
print("equity unchanged, payables +40 in year 1 only:", round(base, 4), "->", round(pay, 4), "rises:", pay > base)
# Check 3: equal dollar increase, borrowing (cash up) vs payables (inventory up): TA rises by the same 40 either way.
borrow = factor(400.0, 100.0, 440.0, 100.0)
print("borrowing +40 and payables +40 give the same factor:", borrow == pay)
# Check 4: the condition matters: equity rising with a liability rise can leave the factor lower.
cond = factor(400.0, 100.0, 440.0, 140.0)
print("liability +40 with equity +40 (both years end at new level): factor", round(cond, 4), "vs base", round(base, 4), "rises:", cond > base)
