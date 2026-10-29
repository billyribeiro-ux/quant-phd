from fractions import Fraction as F
import numpy as np
def g0(nu):
    a=F(3,2)-nu; b=F(1,5)-nu
    return -F(1,3)*(a*a-a*b+b*b)-nu
xs=np.linspace(-1,0,1000001)
vals=-(1/3)*((1.5-xs)**2-(1.5-xs)*(0.2-xs)+(0.2-xs)**2)-xs
i=int(np.argmax(vals)); print("L04 R3 continuous max nu=",xs[i],"value",vals[i],"claimed -209/400 =",-209/400)
print("g0(-3/5)=",g0(F(-3,5)),"g0(-7/10)=",g0(F(-7,10)),"-157/300=",F(-157,300),"grid gap",F(-1,2)+F(157,300))
print("grid values nu=-k/10:",[str(g0(F(-k,10))) for k in range(0,11)])
print("mu'Sinv mu", F(199,150))
# L06 exact recomputation (independent code)
import numpy as np
M=[[0]*4 for _ in range(4)]
