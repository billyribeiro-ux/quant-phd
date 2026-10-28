import numpy as np
from fractions import Fraction as F
Q=np.array([[4,1,0],[1,3,1],[0,1,2]],float); c=np.array([-1,0,2],float)
A=np.array([[1,1,1],[0,1,-1]],float); b=np.array([1,0],float)
K=np.block([[Q,A.T],[A,np.zeros((2,2))]])
print("det K", round(np.linalg.det(K),9))
sol=np.linalg.solve(K,np.concatenate([-c,b])); print("x",sol[:3]*19,"lam",sol[3:]*19)
v=np.array([-2,1,1.]); print("v'Qv",v@Q@v, "Av",A@v)
x=sol[:3]; f=lambda z: 0.5*z@Q@z+c@z
print("obj",f(x), 551/722)
# Part B
QB=np.array([[2,1],[1,2.]]); cB=np.array([-3,1.])
g=np.linspace(0,2,33); best=min(f2 for f2 in (0.5*np.array([a,bb])@QB@np.array([a,bb])+cB@np.array([a,bb]) for a in g for bb in g))
print("grid min",best, "claimed -9/4")
# Remark 2.4 decomposition check
import random
for _ in range(3):
    x3=np.random.randn(3); lhs=x3@Q@x3
    rhs=(2*x3[0]+x3[1]/2)**2+11/4*(x3[1]+4/11*x3[2])**2+18/11*x3[2]**2
    print("decomp diff", lhs-rhs)
