from decimal import Decimal
import math
# L02 Section 6: PV at 8% of WC flows -690, +10, 0, +680 at periods 1..4
pv = -690/1.08 + 10/1.08**2 + 0/1.08**3 + 680/1.08**4
print("L02 WC PV at 8% unrounded:", round(pv, 4), "rounded:", round(pv, 2))
# L02 Example: NPV of incremental flows at 8%
flows = [-12000, 3135, 4360, 3600, 4130]
npv = sum(f / 1.08**t for t, f in enumerate(flows))
print("L02 NPV at 8%:", round(npv, 2), "minus sunk:", round(npv - 2000, 2))
# L02 OCF_1 and identity
print("L02 OCF1:", 4100*0.75 + 0.25*3000, "EBIT1 tax", 0.25*1100)
# L02 P1 / M3 numbers
print("L02 M3 incremental NPV:", round(-2000 + 1200/1.1 + 1200/1.21, 4), "charged:", round(-2000 + 1200/1.1 + 1200/1.21 - 500, 4))
# L02 M2 WC flows
print("L02 M2 nwc flows:", [-160, -40, 0, 200], sum([-160, -40, 0, 200]))
# L02 M1: shield and OCF
print("L02 M1 shield, OCF:", 0.30*200, 500*0.70+60)
# L01 Example 1.2
f = [-10000, 3000, 3200, 3400, 3600, 3800]
print("L01 Ex1.2 NPV 8% unrounded:", round(sum(x/1.08**t for t,x in enumerate(f)), 4))
terms=[3000/1.08,3200/1.08**2,3400/1.08**3,3600/1.08**4,3800/1.08**5]
print("L01 terms:", [round(t,2) for t in terms], "sum", round(sum(terms),4))
print("L01 Remark1.3 4-place factors:", sum(round(3000*round(1.08**-t,4),2) for t in range(1,6)))
# L01 Remark 5.2
print("A(0.10,3):", (1-1.1**-3)/0.10, "with rounded 0.7513:", (1-0.7513)/0.10)
print("Example 5.3:", 120*2.486852)
# L01 M1
print("M1:", -100+60/1.1+60/1.21, [round(60/1.1,4), round(60/1.21,4)])
# L01 M2
A=(1-1.06**-4)/0.06; print("M2 A:", A, "NPV", -500+150*A)
# L01 M3
print("M3:", -200+120+120, -200+120/1.2+120/1.44)
# L01 P-misc: per-dollar ranking
print("L01 Section7 E:", -1000+600+600, -1000+600/1.2+600/1.44)
# R3
print("R3:", -1+1.05/1.06, -1+1.05/1.03)
# c014/c110 n/a; c001 n/a
