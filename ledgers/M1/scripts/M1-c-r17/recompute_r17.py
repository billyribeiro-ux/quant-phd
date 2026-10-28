import math
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50
def pv_ann(c, r, n): return c*(1-(1+r)**-n)/r
print("L07 Ex1.3 closed:", round(100*(1-1/1.331)/0.1,4), "direct:", round(100/1.1+100/1.21+100/1.331,4))
print("L07 Ex1.5 due:", round(1.1*248.6852,4), "diff", round(1.1*248.6852-248.6852,4))
print("L07 Ex2.5 ten:", 100*(1-1.05**-10)/0.05, "gap:", 2000*1.05**-10, "sum", 100*(1-1.05**-10)/0.05+2000*1.05**-10)
q=1.03/1.08
print("q",q,"PV1",100/1.08,"PV10 closed", 2000*(1-q**10), "rem10", 2000*q**10)
print("M1 L07:", 200*(1-1.06**-5)/0.06, 200*(1-1.06**-5)/0.06)
print("1.06^5", 1.06**5, "1.06^-5", 1.06**-5)
print("E1 L07 ln:", math.log(2000)/math.log(1.08/1.03), math.log(1.08/1.03))
print("m for exact gap<=1:", math.log(2000)/math.log(1.05), "P3 bound m:",1999/0.05)
print("E2 30y 5%:", pv_ann(100,0.05,30), "10%:", pv_ann(100,0.10,30))
print("L07 q=1.03/1.08 N=160 gap", 2000*q**160, "N=161", 2000*q**161)
print("L07 Misc: (1.05)*2000", 1.05*2000, " M3 L07:", 100/0.06, 100/0.06*1.1)
print("L06 M3 S4,S5:", 2*(1-2**-4), 2*(1-2**-5))
print("L06 E2 numbers: q=1+1e-9 n60 numerator", 1-(1+1e-9)**60, "q=1.001 numerator", 1-1.001**60)
print("L06 E2 ratio est", 1e-16/abs(1-(1+1e-9)**60), 1e-16/abs(1-1.001**60))
print("L06 misc poly:", [n*n+n+41 for n in (40,)], 1681==41*41)
# primality n^2+n+41 for 0..39
def isprime(x):
    if x<2: return False
    i=2
    while i*i<=x:
        if x%i==0: return False
        i+=1
    return True
print("euler prime 0..39:", all(isprime(n*n+n+41) for n in range(40)))
# L08
i=F(6,100)/12; n=360; L=250000
A=L*i/(1-(1+i)**-n)
print("exact pay", float(A))
def half_up(x): return math.floor(x+F(1,2))
PC=25_000_000
regular=half_up(F(PC)*0+A*100)  # A in CU -> cents
A_cents=A*100
print("A cents", float(A_cents), "regular cents", half_up(A_cents))
reg=half_up(A_cents)
rows=[]; bal=PC; 
for k in range(1,n+1):
    I=half_up(F(bal)*i)
    pay = reg if k<n else bal+I
    p=pay-I; cl=bal-p
    rows.append((k,bal,I,p,pay,cl)); bal=cl
print("final pay cents", rows[-1][4], "final I", rows[-1][2], "row 359", rows[-2], "row1", rows[0], "row2", rows[1], "row3", rows[2])
print("total interest", sum(r[2] for r in rows)/100, "total paid", sum(r[4] for r in rows)/100)
def exact_bal(k, Acents): return PC*(1+i)**k - Acents*((1+i)**k-1)/i
drift=max(abs(r[5]-half_up(exact_bal(r[0],F(reg)))) for r in rows[:-1])
print("drift rounded-reg (cents)", drift)
ex=[ (abs(r[5]-exact_bal(r[0],A_cents)), r[0]) for r in rows[:-1]]
mx=max(ex); print("max gap vs exact-payment (cents)", float(mx[0]), "at month", mx[1])
first=[r[0] for r in rows[:-1] if abs(r[5]-exact_bal(r[0],A_cents))>=100]
print("first >=1CU month", first[0])
idm=[r[0] for r in rows[1:-1] if r[3]==(1+i)*rows[r[0]-2][3]]
print("identity months", idm, len(rows[1:-1]))
# exact interest variant
e=F(PC)
for _ in range(359): e=e*(1+i)-reg
print("final if exact interest (cents reg)", float(e*(1+i))/100)
print("1.005^360", float((1+i)**360), "factor", float(((1+i)**360-1)/i))
print("exact pay - reg cents", float(A_cents-reg))
print("month360 exact-rounded-reg balance", float(F(PC)*(1+i)**360 - F(reg)*((1+i)**360-1)/i)/100)
print("R3 -0.003687118*1004.5150425", (float(A_cents-reg)/100*float(((1+i)**360-1)/i)))
print("R3 gap check 1498.88-1495.18", 1498.88-1495.18, "1498.88-1495.45", 1498.88-1495.45)
print("eff annual", float((1+i)**12-1))
print("E1 5pct", 250000*(F(5,100)/12)/(1-(1+F(5,100)/12)**-360), float(250000*(F(5,100)/12)/(1-(1+F(5,100)/12)**-360)))
print("E2 shares", 1250/1498.88*100, 7.44/1495.45*100)
print("M1 L08", 10000*0.01/(1-1.01**-12), 1.01**12, 1.01**-12, 1-1.01**-12)
A10=10000*0.01/(1-1.01**-12)
print("M2 p1", A10-100, "B1", 10000-(A10-100), "M3 p2", 1.01*(A10-100), "I2", 0.01*(10000-(A10-100)), A10-0.01*(10000-(A10-100)))
print("P3 total int", 12*A10-10000)
print("R2 1.005^360", float((1+i)**360), (1.005**360-1)/0.005, 0.005*(1.005**360-1)/0.005)
print("R2 month 360 bal", -0.005*(1.005**360-1)/0.005, "1.80", 0.005*360)
print("E3", 1.005**12-1)
print("Q L08 8 check 0.005", 0.06/12)
print("L08 misc 72%", 0.06*12)
print("Section canon 1.005^12", 1.005**12)
print("E2 month360 share", 7.44/1495.45)
