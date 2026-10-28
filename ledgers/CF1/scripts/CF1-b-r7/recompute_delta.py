from fractions import Fraction as F
# L04 Example 3.2 / Prop 3.3 profile
P = lambda r: -100000 + F(230000)/(1+r) - F(132000)/(1+r)**2
for r in [F(0), F(5,100), F(10,100), F(15,100), F(20,100), F(25,100), F(30,100)]:
    print("P", float(r), float(P(r)))
print("factorization equal at test rates:", all(P(r) == -2000*(11/(1+r)-10)*(6/(1+r)-5) for r in [F(-4,10), F(0), F(5,100), F(15,100), F(1,2), F(2)]))
# crossover A,B (USD)
A = lambda r: -100000 + F(130000)/(1+r)
B = lambda r: -200000 + F(250000)/(1+r)
print("crossover", A(F(1,5)) == B(F(1,5)), "NPV A/B at 0.10", float(A(F(1,10))), float(B(F(1,10))))
print("sign at 0.05,0.10,0.15,0.20,0.25,0.30 of A-B:", [ (float(r), float(B(r)-A(r))) for r in [F(5,100),F(1,5),F(3,10)]])
# Example 2.5 nominal and real
nom = sum(F(100)/F(108,100)**t for t in (1,2,3)); print("ex2.5 nominal NPV", float(nom))
print("real rate", float(F(108,100)/F(103,100)-1))
# L03 shares
print("E1 share 0.05", 194368.27/263709.14, "0.01", 36913.22/263709.14, "0.03", 113637.49/263709.14)
# L03 R2 ratio
print("R2 ratio", 0.06*1.03/0.03)
# L04 R1 NPV at 10%
print("R1 NPV10", -1 + 6/1.1 - 5/1.21)
# L04 R2 example
print("R2 IRR_A", 3**0.5-1, "NPV_A", 300/1.21-100, "NPV_B", 200/1.1-100)
# R3 FV
print("FV15", 1.15**2*189.036, "FV5", 1.05**2*(-680.272))
# L03 l.248 two-line example
print("implied n", 205*1.05/200-1, "implied infl", (205*1.05/200)/1.05-1)
# L03 P3 sqrt
print("P3", 0.005**0.5)
# L03 R3 b
print("R3 b", 1.06/2.03)
