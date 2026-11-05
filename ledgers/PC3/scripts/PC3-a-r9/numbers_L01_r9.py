import math
from fractions import Fraction as F
# E2 (L01.html:408): four-place quotient vs full precision
print("E2 four-place quotient 0.9163/2.9704 =", 0.9163/2.9704, "pct", 100*0.9163/2.9704)
base = math.log(19.5)
red_q = 0.9162907319
red_m = 0.1753528875
print("E2 full-precision base ln19.5 =", base)
print("E2 quote share =", red_q/base, "pct", 100*red_q/base)
print("E2 minutes share =", red_m/base, "pct", 100*red_m/base)
# Example 1.4 and E3
print("ln19.5", math.log(19.5), "ln3", math.log(3), "ln5", math.log(5), "ln1.3", math.log(1.3))
print("ln16.5", math.log(16.5), "diff", math.log(19.5)-math.log(16.5))
print("geo mid", math.sqrt(12000*234000))
# Example 1.7
n, x = 10, F(1,100)
rem = (1+x)**n - 1 - n*x
bound = F(n*(n-1),2)*(1+x)**(n-2)*x*x
print("ex1.7 exact", float((1+x)**n), "rem", float(rem), "bound", float(bound))
print("ratio rem/bound", float(rem/bound), "bound/rem-1", float(bound/rem)-1)
x=F(1,20)
print("x=1/20 exact", float((1+x)**10), "rem", float(((1+x)**10)-1-10*x), "bound", float(F(45)*(1+x)**8*x*x), "miss/exact", float(((1+x)**10-1-10*x)/((1+x)**10)))
# Quiz Q9
print("sqrt", math.sqrt(2808000000))
# Q6 remainder
print("Q6", float(F(1,1)*((F(101,100))**10)-1-F(10,100)))
# R1 ln5 vs half
print("half total", base/2, "ln5", math.log(5))
# R3
print("R3 ln(2.5/1.01)", math.log(2.5/1.01), "ln(3/2)", math.log(1.5), "ln3", math.log(3), "ln2.5", math.log(2.5))
# Lab Part 2 narrowing check
print("narrow quote", math.log(19.5)-math.log(2.0541237337))
