from fractions import Fraction as F
import math
def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def det2(m): return m[0][0]*m[1][1]-m[0][1]*m[1][0]
def inv2(m):
    d = det2(m); return [[F(m[1][1], d), F(-m[0][1], d)], [F(-m[1][0], d), F(m[0][0], d)]]
A = [[4,1],[1,3]]
print("det(A-4I)", det2([[0,1],[1,-1]]), "det(A-3I)", det2([[1,1],[1,0]]))
print("lam+ ,lam- =", (7+math.sqrt(5))/2, (7-math.sqrt(5))/2, "rounded", f"{(7+math.sqrt(5))/2:.4f}", f"{(7-math.sqrt(5))/2:.4f}")
R = [[0,-1],[1,0]]
print("R check: p(lambda)=lambda^2+1 at lambda=0:", det2([[0,-1],[1,0]]))
P = [[1,1],[0,-1]]; D3 = [[27,0],[0,1]]; D = [[3,0],[0,1]]
Pi = inv2(P)
A1 = [[3,2],[0,1]]
print("P^-1 =", Pi, "A = PDP^-1 ?", mul(mul(P,D),[[Pi[i][j] for j in range(2)] for i in range(2)]) == [[3,2],[0,1]])
print("A^3 via PD^3P^-1", mul(mul(P,D3),[[Pi[i][j] for j in range(2)] for i in range(2)]))
A2 = mul(A1,A1); print("A^3 direct", mul(A2,A1))
M2 = [[2,1],[-1,2]]; print("M3 det P", det2(M2), "P^-1", inv2(M2))
