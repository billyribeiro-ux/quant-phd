from fractions import Fraction as F
import math
P=25_000_000; i=F(6,100)/12; n=360
def half_up(x): return math.floor(x+F(1,2))
A=P*i/(1-(1+i)**-n)
reg=half_up(A)
# cent schedule
bal=P; cs=[]
for k in range(1,n+1):
    it=half_up(F(bal)*i); pay=reg if k<n else bal+it
    cl=bal-(pay-it); cs.append((k,bal,it,pay,cl)); bal=cl
# exact-with-rounded-regular-payment balances
def eb(k,pay): g=(1+i)**k; return P*g-pay*(g-1)/i
e=[eb(k,F(reg)) for k in range(0,n+1)]
# unrounded-interest final payment with regular payment
b=F(P)
for k in range(1,n): b=b*(1+i)-reg
print("exact-rounded balance at 360 (cents):", float(e[360]))
print("exact-rounded final payment needed:", float(b*(1+i)))
print("cent final payment:", cs[-1][3])
print("final gap regular-final:", reg-cs[-1][3])
# excess compounding: reg - A per payment, FV
ex=F(reg)-A
print("excess per payment (CU):", float(ex/100), " FV at 360 (CU):", float(ex*((1+i)**n-1)/i/100))
# drift without comparison rounding, and with
d=[]
for k,bal_,it,pay,cl in cs[:-1]:
    d.append((k, cl-e[k]))
mx=max(d,key=lambda t:abs(t[1]))
print("max unrounded drift (cents) vs exact-rounded:", float(abs(mx[1])), "at", mx[0])
print("max printed-style drift:", max(abs(cl-half_up(e[k])) for k,_,_,_,cl in cs[:-1]))
print("month 360 exact-rounded balance (CU):", float(e[360]/100))
# identity of interest rounding: d_k recurrence check
