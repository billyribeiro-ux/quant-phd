"""Independent exact recomputation of the L01 numbers (Examples, M1-M3, E1-E3, R3, misconceptions, quiz) and Lab 1 Part A/B/C values."""
from fractions import Fraction as F

def ev(l): return sum(p*x for x, p in l)
def eu(l, u): return sum(p*u(x) for x, p in l)
lin = lambda x: F(x)
quad = lambda x: F(x*x, 10000)
A = [(0, F(1,4)), (10000, F(1,2)), (40000, F(1,4))]
B = [(5000, F(1,2)), (20000, F(1,2))]
C = [(0, F(1,3)), (15000, F(1,3)), (30000, F(1,3))]
for n, L in (("A", A), ("B", B), ("C", C)):
    print("lab", n, "EV cents", ev(L), "EU lin", eu(L, lin), "EU quad", eu(L, quad))
print("Ex1.4 EV CU", ev([(0,F(1,4)),(100,F(1,2)),(400,F(1,4))]), "quad CU2", sum(p*x*x for x,p in [(0,F(1,4)),(100,F(1,2)),(400,F(1,4))]))
print("M1 EV", 20*F(1,5)+50*F(3,10)+80*F(1,2), "EU", 400*F(1,5)+2500*F(3,10)+6400*F(1,2), "u(59)", 59*59, "diff", (400*F(1,5)+2500*F(3,10)+6400*F(1,2))-59*59)
print("M2 mixture weights", F(1,3)*F(1,2), F(1,3)*F(1,2)+F(2,3)*F(1,4), F(2,3)*F(3,4), "EU mix", F(100,3)+100, "RHS", F(1,3)*50+F(2,3)*175)
print("M3 X", (10+30)/2, "Y", 0*F(1,4)+40*F(3,4), "v", 5+3*20, 5+3*30)
print("C (Ex3.4) quad", eu(C, lambda x: F(x*x)), "vs A quad 45000 CU2 in CU units")
print("E2 line", F(1,3)*45000+F(2,3)*37500)
print("E3 check sums", F(1,2)+F(1,2)*0 - 0, F(1,2)+F(1,3), F(-1,2)+F(3,2))
print("R3 X EU", (100**2+200**2)/2, "Y", 150**2)
print("quiz q7 P(0)", F(1,3)*F(1,4)+F(2,3)*F(1,2), "quiz q10", F(200,4))
print("misc: 3481 check", 59**2, "CE u(150)", 150**2)
print("prize shares Ex1.4 q1", 0*F(1,4)+100*F(1,2)+400*F(1,4))
