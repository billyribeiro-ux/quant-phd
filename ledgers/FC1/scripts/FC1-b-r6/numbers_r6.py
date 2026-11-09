from fractions import Fraction as F
import datetime
G = 68398886; NP = 14282414; P5 = 11060360
print("NP/G exact", float(F(NP, G)), "to 8dp", f"{NP/G:.8f}", "to 5dp", f"{NP/G:.5f}", "to 3dp half-up", F(NP,G)*1000)
q = F(NP, G)
import math
print("1000*q + 1/2 floor", math.floor(1000*q + F(1,2)))
print("P5/G", float(F(P5,G)), f"{P5/G*100:.4f} %")
print("P5/NP", float(F(P5,NP)), f"{P5/NP*100:.4f} %")
print("216*10060", 216*10060)
print("sum neg", 7411991+6656379+214044, "pos", 3222054+11060360, "sum all", -7411991-6656379+3222054-214044+11060360)
print("net sums", -7411991-6656379+3222054-214044+11060360)
print("2026-10-28", datetime.date(2026,10,28).strftime('%A'), "2026-10-30", datetime.date(2026,10,30).strftime('%A'), "2026-11-02", datetime.date(2026,11,2).strftime('%A'))
print("1060", F(159000,150), "5600/173", F(5600,173), float(F(5600,173)))
print("1000*60+1100*90", 1000*60+1100*90)
print("M1", 60*995+40*990, F(99300,100))
print("1009000/100", 100*10090)
print("0.2088 tolerance check", float(q))
