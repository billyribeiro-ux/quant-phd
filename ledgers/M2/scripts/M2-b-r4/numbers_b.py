"""Recompute the explicit numbers that slice-b pages and cards state (unrounded, exact where possible)."""
from fractions import Fraction as F
import math
print("L07 2.4: 10/7 - 1.3 =", float(F(10,7)-F(13,10)), " 9/70 =", float(F(9,70)), " (3/10)^11/(7/10) =", float((F(3,10)**11)/(F(7,10))))
print("L07 E1 ratio e5/e4 =", 0.0010414286/0.0034714286, "exact ratio e5/e4 = 0.3")
print("L07 E2 (2/3)(1/2)^9 =", (2/3)/512, " (2/3)(1/2)^10 =", (2/3)/1024)
print("L07 E3 errors: x=3/10 -> ", float(F(3,10)**11/F(7,10)), " x=-1/2 ->", float(F(-1,2)**11/F(3,2)), " x=2 ->", float(F(2)**11/F(-1)))
print("L07 R2 2^19, 2^20 vs 1e6:", 2**19, 2**20, 10**6)
print("L08 ex2.3/M2: xi(1/4,n=2) =", 1-(0.75)**0.25)
print("L08 E1: (1/2)^(1/5) =", 0.5**0.2, " xi =", 1-0.5**0.2)
print("L08 E2: (0.7)^(1/7) =", 0.7**(1/7), " xi =", 1-0.7**(1/7))
print("L08 Remark3.3 bounds:", [0.6**(n+1)/0.4**(n+2) for n in range(1,5)], " exact:", [0.6**(n+1)/0.4 for n in range(1,5)])
print("L08 Example 2.4 ratio check x=0.3: ", 2**4*(1-0.3))
print("L08 R3 bound at 1/2:", [2**(n+2)*0.5**(n+1) for n in range(0,4)])
# L09 part B: nonuniform partition points (i/10)^2
n=10
pts=[F(i*i,n*n) for i in range(n+1)]
w=[pts[i]-pts[i-1] for i in range(1,n+1)]
U=sum(float(pts[i]**2)*float(w[i-1]) for i in range(1,n+1))
L=sum(float(pts[i-1]**2)*float(w[i-1]) for i in range(1,n+1))
print("L09 B: mesh", float(max(w)), " U-L exact =", float(sum((pts[i]**2-pts[i-1]**2)*w[i-1] for i in range(1,n+1))), " U-L float", U-L)
print("L09 E3: n=50 bound", 151/15000, " n=51 bound", 154/15606, " 1/n test n=100:", 1/100)
print("L09 E1: 25/384 =", 25/384, " E2: 1/3072 =", 1/3072, " 385/98304 =", 385/98304, " U128-1/3 =", 0.33724976-1/3)
print("L09 Remark: midpoint err n=8 -1/768 =", -1/768, " n=16 -1/3072 =", -1/3072, " n=32 -1/12288 =", -1/12288)
# L10 E3 truncation estimate
print("L10 E3: F'''(0.3)=6/1.3^4 =", 6/1.3**4, " h^2F'''/6 =", 1e-12*6/1.3**4/6)
print("L10 E2: 3/512 =", 3/512, " L128 printed diff", 0.50293859-0.49707921)
print("L10 E1: U8-L8 printed", -0.80468750-(-1.17968750), " 3/8 =", 3/8)
print("L10 Example 3.2 integral: (1-2)-0 =", (1-2))
print("L10 misc: G(1)=", 1/2+5, " F(1)-F(0)=", 1/2)
# L11
print("L11 E1: N^2>=2/(3e-6) ->", 2/(3e-6), " N=816 err", 2/(3*816**2), " N=817 err", 2/(3*817**2))
print("L11 E2: 8/3 - 2.6666666663 =", 8/3-2.6666666663)
print("L11 Ex2.2 int x(1-x)^4 =", 1/2-4/3+3/2-4/5+1/6, " int x^2(1-x)^3 =", (1/2)*(1/30))
print("L11 M3: int x^3(1-x) =", F(1,4)-F(1,5), " 3/2*(1/30)=", F(3,2)*F(1,30))
print("L11 M2 expansion 2t+4t^3+2t^5 int =", 1+1+2/6, " 7/3=", 7/3)
print("L11 Ex3.2: 3/9+7/7+5/5+1/3 =", F(3,9)+F(7,7)+F(5,5)+F(1,3), " 8/3=", F(8,3))
print("L11 Ex3.3: int (2t+2t^3) =", F(2,2)+F(2,4), " (4-1)/2=", F(3,2))
print("L11 R3: 1/2 vs 2/4", F(1,2), F(2,4))
# L12
print("L12 H_N-1 values:", [round(sum(1/i for i in range(2,2**m+1)),8) for m in (1,4,8,12,14)])
print("L12 E3: 9.28130671-7 =", 9.28130671-7)
print("L12 E2 1/b at 1e6 =", 1e-6)
