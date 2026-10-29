import math, random
# L05 ratio and displayed quotients
print("L05 ratio", 0.0010539032/0.0002187758)
print("L05 E1 rel", (0.00039491-0.0004)/0.0004, "E2 errs", 0.0004-0.00038490, 0.00036-0.00033176, 0.0009-0.00073743)
print("L05 corr err", 0.592936-0.6)
# L06
print("L06 rel5", (1.669114-5/3)/(5/3), "rel10", (1.240325-1.25)/1.25, "ratio E2", 0.007740/0.001469, 0.00774/0.001468)
print("L06 E3", (4.997415-5)/5, "E1", (1.669114-1.666667)/1.666667)
print("L06 sqrt(2/pi)", math.sqrt(2/math.pi), "e^3", math.exp(3), "e^.5", math.exp(0.5))
# L07 modulus
p=0.25;q=0.75
v=p*p+q*q+2*p*q*math.cos(-2)
print("L07 |phi(1)|^2", v, "sqrt", math.sqrt(v), "realpart", p+q*math.cos(2))
print("L07 E2 rel", 7.11e-13/244.69193226)
print("L07 E1 diff", -0.062124-(-0.062110))
