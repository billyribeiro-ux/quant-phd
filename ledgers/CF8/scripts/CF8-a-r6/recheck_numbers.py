from fractions import Fraction as F
import math
# L02 Part A
def simple(d,e,l): return d/(1-d)*F(365,l-e)
def comp(d,e,l):
    f=float(1/(1-d)); return f**(365/(l-e))-1
for lab,d,e,l in [("2/10 n30",F(2,100),10,30),("1/10 n30",F(1,100),10,30),("2/10 n60",F(2,100),10,60),("3/15 n45",F(3,100),15,45),("fin",F(5,1000),10,60)]:
    print(lab, float(simple(d,e,l))*100, comp(d,e,l)*100)
# L02 Part B
rev=F(12_000_000); dold,dnew=30,45; ext=F(1_500_000); r=F(1,10); n=5
inv=((rev+ext)*dnew - rev*dold)/365
print("dI", float(inv))
ms=r*inv/ext; print("m*", float(ms))
def npv(m,base,I,years):
    A=sum((1/(1+r))**t for t in range(1,years+1))
    return -I+m*base*A+I/(1+r)**years
print("NPV 5% over5", float(npv(F(5,100),ext,inv,5)))
print("NPV at m*", npv(ms,ext,inv,5))
# M2/M3 (rate 8%, horizon 4)
def npvr(m,base,I,years,rate):
    A=sum((1/(1+rate))**t for t in range(1,years+1))
    return -I+m*base*A+I/(1+rate)**years
I2=F(216_000_000,365); print("M2 dI", float(I2), "m*", float(F(8,100)*I2/600000))
A4=sum((1/F(108,100))**t for t in range(1,5)); print("A(.08,4)", float(A4))
t1=-I2; t2=F(10,100)*600000*A4; t3=I2/F(108,100)**4
print("M3 terms", float(t1), float(t2), float(t3), "sum", float(t1+t2+t3))
# E2
I3=F(390_000_000,365); print("E2 dI", float(I3), "m*", float(F(9,100)*I3/2_000_000))
A3=sum((1/F(109,100))**t for t in range(1,4)); print("A(.09,3)", float(A3))
print("E2 NPV", float(-I3+F(6,100)*2_000_000*A3+I3/F(109,100)**3))
# E1
print("E1 costs", float(simple(F(2,100),10,30))*100, float(simple(F(1,100),15,45))*100, float(simple(F(2,100),10,60))*100)
# M1 2
print("M1 c", float(F(1,100)/F(99,100)*F(365,30))*100)
# R1
print("R1 mnr", float(F(1)*I2/(600000*A4)), float(F(8,100)*0+ (I2/(600000*A4))/(F(8,100)*I2/600000)))
print("R1 ratio", float(1/(1-F(1,1)/F(108,100)**4)))
# Ex1.4
print("ex1.4 simple", float(F(2,100)/F(98,100)*F(365,20)), comp(F(2,100),10,30))
# Remark 2.2 etc done; Lab A printed "compounded" check values with page
