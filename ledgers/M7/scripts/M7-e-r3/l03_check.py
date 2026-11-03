from fractions import Fraction as F
S=[[F(2),F(1)],[F(1),F(2)]]
def f(w,mu):
    q=sum(w[i]*S[i][j]*w[j] for i in range(2) for j in range(2))/2
    return q-(mu[0]*w[0]+mu[1]*w[1])
for mu in [(F(3,2),F(1,5)),(F(1),F(1))]:
    vals=[(f((F(k,100),1-F(k,100)),mu),k) for k in range(101)]
    m=min(vals)
    print("mu",mu,"grid min",m[0],"at w1=",F(m[1],100), "count", len(vals), "ties", sum(1 for v in vals if v[0]==m[0]))
print("candidate f(1,0) active", f((F(1),F(0)),(F(3,2),F(1,5))), "f(1/2,1/2) inactive", f((F(1,2),F(1,2)),(F(1),F(1))))
print("f(3/5,2/5) inactive", f((F(3,5),F(2,5)),(F(1),F(1))))
print("f(1/2,1/2) active", f((F(1,2),F(1,2)),(F(3,2),F(1,5))))
import math
print("norm (-1/2,1/2)", math.sqrt(0.25+0.25), round(math.sqrt(0.5),4))
# (x^2-1)^2 check not needed
# Example 4.1 KKT residuals exact
w=(F(1),F(0)); mu=(F(3,2),F(1,5)); nu=F(-1,2); lam=(F(0),F(3,10))
grad=[S[i][0]*w[0]+S[i][1]*w[1]-mu[i] for i in range(2)]
K1=[grad[0]+lam[0]*(-1)+nu, grad[1]+lam[1]*(-1)+nu]
print("grad",grad,"K1 residual",K1)
# Example 4.1 check: candidate is minimizer on grid also at w2 only

# Example 4.1 / lab residual claims: stationarity residual at (1/2,1/2) with active multipliers; dual residual for lambda2=-3/10
nu=F(-1,2); lam=(F(0),F(3,10))
w=(F(1,2),F(1,2))
gradf=[S[i][0]*w[0]+S[i][1]*w[1]-mu[i] for i in range(2)]
K1=[gradf[0]+lam[0]*(-1)+nu, gradf[1]+lam[1]*(-1)+nu]
print("stationarity residual at (1/2,1/2):",K1)
print("dual residual with lambda2=-3/10:", -F(-3,10))
