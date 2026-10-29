import math
from fractions import Fraction
b=math.sin(1.0)
print("ratio5", 2.661258/0.05439523)
print("cos(0.995)-cos1 over .005", (math.cos(0.995)-math.cos(1))/0.005)
print("sin1 - that", b-(math.cos(0.995)-math.cos(1))/0.005)
print("n90.71", math.log(1/(1e-6*(1-b)))/math.log(1/b))
for n in range(85,95):
    if b**n/(1-b)<=1e-6: print("first n", n); break
print("f'(5)", 5/math.sqrt(26), "f'(50)", 50/math.sqrt(2501))
print("0.99^1000", 0.99**1000, "0.99^100", 0.99**100, "0.99^10", 0.99**10)
print("exact 0.99^1000 via Fraction->float", float(Fraction(99,100)**1000))
print("bound n5", b**5/(1-b), "err5 check", abs(math.cos(math.cos(math.cos(math.cos(math.cos(0.0)))))-0.739085133))
print("E1 bound", b**5/(1-b))
