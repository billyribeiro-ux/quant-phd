"""Round-2 exact checks: Proposition 3.1 (STD=0), Proposition 4.1 (scale invariance), and P3's assumption claim."""
import random
from fractions import Fraction as F

rng = random.Random(5)
def r():
    return F(rng.randint(-2000, 2000), rng.randint(1, 60))

bad31 = 0
bad41 = 0
for _ in range(3000):
    cash0, cash1, cao0, cao1, ppe0, capex, da, onca0, onca1, oncl0, oncl1, cl0, cl1, ltd0, ltd1, D = (r() for _ in range(16))
    ppe1 = ppe0 + capex - da
    ta0 = cash0 + cao0 + ppe0 + onca0; ta1 = cash1 + cao1 + ppe1 + onca1
    E0 = ta0 - (cl0 + ltd0 + oncl0); E1 = ta1 - (cl1 + ltd1 + oncl1)
    NI = E1 - E0 + D
    CFO = (cash1 - cash0) + capex - (ltd1 - ltd0) + D
    noa0 = cao0 + ppe0 + onca0 - cl0 - oncl0
    noa1 = cao1 + ppe1 + onca1 - cl1 - oncl1
    bad31 += (NI - CFO) != (noa1 - noa0) - capex
    # Prop 4.1: scale every money item by k; both measures unchanged
    k = F(rng.randint(1, 500), rng.randint(1, 50))
    def meas(x):
        cash0_, cash1_, cao0_, cao1_, ppe0_, ppe1_, onca0_, onca1_, oncl0_, oncl1_, cl0_, cl1_, ltd0_, ltd1_, NI_, D_, da_, capex_ = x
        ta0_ = cash0_ + cao0_ + ppe0_ + onca0_; ta1_ = cash1_ + cao1_ + ppe1_ + onca1_
        avg = (ta0_ + ta1_) / 2
        cfo = (cash1_ - cash0_) + capex_ - (ltd1_ - ltd0_) + D_
        cf = (NI_ - cfo) / avg
        bs = ((cao1_ - cao0_) - ((cl1_) - (cl0_)) - da_) / avg
        return cf, bs
    base = [cash0, cash1, cao0, cao1, ppe0, ppe1, onca0, onca1, oncl0, oncl1, cl0, cl1, ltd0, ltd1, NI, D, da, capex]
    scaled = [k * v for v in base]
    if meas(base) != meas(scaled):
        bad41 += 1
print("Prop 3.1 (A1-A4, STD=0): NI-CFO = dNOA - capex failures in 3000:", bad31)
print("Prop 4.1 scale invariance failures in 3000 exact draws:", bad41)

# P3 claim: 'The one assumption not in Proposition 2.2 is STD_t = 0'.
# A3 (page line 99): 'current liabilities carry no debt'. Under A3, STD_t = 0 holds, so STD_t = 0 is already in A1-A4.
print("A3 (L04 line 99) states current liabilities carry no debt, i.e. STD=0 is already inside A1-A4; see grep output in the log")
