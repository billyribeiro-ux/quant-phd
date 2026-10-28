from fractions import Fraction as F
# Witness 1: misconception 3 (L01 line 431): revenue and receivables both change; cycle moves by dDSO in days
Rev0, Rev1 = F(9000000000), F(10000000000)
AR0, AR1 = F(1200000000), F(1300000000)
DIO = F(810000000 * 365, 5490000000)
DPO = F(700000000 * 365, 5600000000)
d0 = AR0 * 365 / Rev0
d1 = AR1 * 365 / Rev1
print("W1 dDSO", float(d1 - d0), "dCCC", float((d1 + DIO - DPO) - (d0 + DIO - DPO)))
# Witness 2: Prop 3.2 (L01 lines 120-126): 'cash released' equals Rev*d/D only if no other balance moves
rel = F(2400000) * 10 / 365
print("W2 AR release", float(rel), "net cash if AP rises 10000 dollars at the same time", float(rel - 10000))
# Witness 3: Remark 4.3 (L02 line 184): DPO moves with payables alone, due date N unchanged
print("W3 dDPO from AP +10000 at purchases 1,600,000, N unchanged", float(F(10000) * 365 / F(1600000)))
# Witness 4: Corollary 3.3 (L02 line 147): dR=0 and N1=N0 gives dI=0, so NPV(m)=0 for every m, not negative
R0, N0, N1 = F(12000000), 30, 30
dI = (R0 * N1 - R0 * N0) / F(365)
print("W4 dI with dR=0, N1=N0", float(dI))
