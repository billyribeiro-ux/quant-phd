from fractions import Fraction
import math, random, itertools, sys
sys.path.insert(0, '/tmp/verifyC2-CF8-b/tests/labs/CF8')
r=[1019781,1057001,875315,1130956,691726,530408,766042,519658,1077355,886624,897559,1072570,1146460]
d=[939544,1070638,918988,924675,1052774,1138473,956281,922530,1009621,963088,1044453,915495,932453]
nu=[a-b for a,b in zip(r,d)]
cum=list(itertools.accumulate(nu))
print("nu6",nu[5],"cum6",cum[5],"L6",1200000+1200000+cum[5],"cum11",cum[10],"U11",600000+cum[10])
print("min nu", min(nu), nu.index(min(nu))+1)
p=Fraction(178,1000)
v=p*(1-p)/2000
print("sqrt", float(v)**0.5, "sqrt(p(1-p)/N)", math.sqrt(0.178*0.822/2000))
print("ratio SE/0.002", math.sqrt(0.178*0.822/2000)/0.002, "N needed", 0.178*0.822/0.002**2)
print("0.146316/0.000004", Fraction(146316,10**6)/Fraction(4,10**6))
print("5*1234567/7", float(Fraction(5*1234567,7)))
# unrounded checks of the M2 digits
print("%.10f" % math.sqrt(0.000073158))
