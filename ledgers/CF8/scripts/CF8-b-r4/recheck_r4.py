"""Round-4 independent re-derivation of every number changed in CF8 L03-L05 (slice b)."""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

# L03 Lab 1 printed table (from /tmp run of tests/labs/CF8/lab-CF8-L03-1.py, stdout md5 b434a24d...)
rec = [1019781,1057001,875315,1130956,691726,530408,766042,519658,1077355,886624,897559,1072570,1146460]
dis = [939544,1070638,918988,924675,1052774,1138473,956281,922530,1009621,963088,1044453,915495,932453]
draw = [0,0,0,0,0,539905,190239,402872,0,76464,146894,0,0]
rep  = [0,0,0,0,0,0,0,0,67734,0,0,157075,214007]
net = [r-d for r,d in zip(rec,dis)]
print("L03 E1 sum of weekly net flows:", sum(net), "expected -1117558 ->", sum(net) == -1117558)
print("L03 E1 closed form:", 1000000-1200000-(1356374-438816))
print("L03 total drawn:", sum(draw), "total repaid:", sum(rep), "check 1356374/438816:", sum(draw)==1356374 and sum(rep)==438816)
print("L03 closing via identity:", 1200000 + sum(net) + sum(draw) - sum(rep))
cum = []; s = 0
for n in net:
    s += n; cum.append(s)
print("L03 w6 P6 =", cum[5]+0 if False else None)
print("L03 w6 cumulative net:", cum[5], "-> 1200000+1200000+cum6 =", 2400000+cum[5], "(L04 line 354 says liquidity 1660095):", 2400000+cum[5]==1660095)
print("L03 w6 net:", net[5], "2nd-check 530408-1138473 =", 530408-1138473)
print("L03 w6 P =", 1068160+530408-1138473)
# L03 Theorem/Example 2.3 P6 uses ending cash before draw:
print("L03 m-P6:", 1000000-460095, "< 4000000:", 1000000-460095 < 4000000)

# L04 numbers
print("L04 corollary constant:", 1200000+1200000-1800000)
print("L04 U11:", 600000-1488640, "printed -888640:", 600000-1488640==-888640)
print("L04 cum flow after week 11 check:", sum(net[:11]), "(expected -1488640):", sum(net[:11])==-1488640)
slip = Decimal(5*1234567)/Decimal(7)
print("L04 slip 5*1234567/7 =", slip, "rounded half-up:", slip.quantize(Decimal('1'), rounding=ROUND_HALF_UP), "printed 881834")
print("L04 pinch after slip:", -888640-881834, "printed -1770474:", -888640-881834==-1770474)
print("L04 example 2.5 U1,U2 check:", 100-60, 100-60-10)

# L05 numbers
p = 0.178
print("L05 M2 SE:", math.sqrt(p*(1-p)/2000), "round4:", round(math.sqrt(p*(1-p)/2000),4))
print("L05 M2 p(1-p)=", round(0.178*0.822,6), "/2000=", 0.178*0.822/2000)
print("L05 M3 ceil(0.05*30)=", math.ceil(F(5*30,100)), " ceil(5*2000/100)=", math.ceil(F(5*2000,100)))
print("L05 E2 buffer 365525/100 =", F(365525,100), float(F(365525,100)), " 99/2000 =", F(99,2000), float(F(99,2000)), " <= 0.05:", F(99,2000)<=F(5,100))
print("L05 R3 p(1-p)/0.002^2 =", 0.146316/0.000004, "ceil:", math.ceil(0.146316/0.000004))
print("L05 R3 SE 2000 years / target:", round(math.sqrt(p*(1-p)/2000),4)/0.002)
print("L05 M2 0.0085532 check:", round(math.sqrt(0.146316/2000),7))
print("L05 Remark 2.4 99/2000 =", 99/2000, "percent:", 99/2000*100)
