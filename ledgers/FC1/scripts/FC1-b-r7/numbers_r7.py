import datetime
from fractions import Fraction as F
# L05 numbers
print("216*10060 =", 216*10060)
print("NP/G =", F(14282414, 68398886), float(F(14282414, 68398886)))
print("NP/G 8dp =", round(14282414/68398886, 8), " 5dp=", round(14282414/68398886, 5))
print("P5/G =", 11060360/68398886*100, "P5/NP =", 11060360/14282414*100)
print("neg sum =", 7411991+6656379+214044, " pos sum =", 3222054+11060360)
print("sum net =", -7411991-6656379+3222054-214044+11060360)
print("2026-10-28 weekday:", datetime.date(2026,10,28).strftime("%A"))
d=datetime.date(2026,10,28); c=0
while c<2:
    d+=datetime.timedelta(days=1)
    if d.weekday()<5: c+=1
print("settle lag2 ->", d, d.strftime("%A"))
d=datetime.date(2026,10,28); c=0
while c<3:
    d+=datetime.timedelta(days=1)
    if d.weekday()<5: c+=1
print("settle lag3 ->", d, d.strftime("%A"))
# L04 numbers
print("E3 5600/173 =", F(5600,173), float(F(5600,173)))
print("E1 24+18 =", 24+18)
print("Ex1.3 cost", 60*1000+90*1100, "avg", F(159000,150))
print("M1 cost", 60*995+40*990, F(99300,100))
print("P2 G", 100+150-100 if False else 250, "R+2X+C", 0+200+50)
print("R3 2*60", 2*60)
# L01 cards check numbers later
