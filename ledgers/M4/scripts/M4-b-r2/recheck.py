import math, random, cmath
# L05 numbers
print("L05 E3 ratio", 0.0010539032/0.0002187758)
print("L05 E1 rel err", (0.00039491-0.0004)/0.0004)
print("L05 E2 errors", abs(0.00038490-0.0004), abs(0.00033176-0.00036), abs(0.00073743-0.0009))
print("L05 Part B err", 0.592936-0.6)
# L06 E1 and unrounded relative error
exec(open('/tmp/verifyB2-M4-b/tests/labs/M4/lab-M4-L06-1.py').read().replace('\nmain()', '\n'))
rng = random.Random(SEED+5); ts=[]
for _ in range(N_DRAWS):
    _, t = chi_square_and_t(rng, 5); ts.append(t)
m, v = mean_and_variance(ts)
print("L06 nu5 unrounded var", repr(v), "rel err", (v-5/3)/(5/3))
print("L06 E1 printed-values rel", (1.669114-1.666667)/1.666667)
print("L06 E2 ratio", 0.007740/0.001469, abs(-0.007740)/0.001469)
print("L06 E3", (4.997415-5)/5)
print("L06 nu10 unrounded")
rng = random.Random(SEED+10); ts=[]
for _ in range(N_DRAWS):
    _, t = chi_square_and_t(rng, 10); ts.append(t)
m10, v10 = mean_and_variance(ts)
print(" mean", m10, "var", v10, "rel", (v10-1.25)/1.25)
print("L06 R1 check sqrt(2/pi)", math.sqrt(2/math.pi), 2/math.sqrt(2*math.pi))
print("L06 q3 1.6666667 vs 5/3", 5/3, abs(5/3-1.6666667))
print("L06 q7", abs(0.7978846-math.sqrt(2/math.pi)))
# L07
print("L07 sqrt", math.sqrt(0.4689449), 0.625+0.375*math.cos(-2), math.sqrt(0.625+0.375*math.cos(-2)))
print("L07 E2", 7.11e-13/244.69193226, 7.11e-13/244.69193226/2.2e-16)
print("L07 e^3", math.exp(3), "e^0.5", math.exp(0.5), "cos2", math.cos(2), 0.25+0.75*math.cos(2))
print("L07 E1 diff", -0.062124-(-0.062110))
print("L07 E3 modulus", math.sqrt(0.25**2+0.75**2+0.375*math.cos(-2)))
print("L07 e^3 tol", abs(math.exp(3)-20.0855))
print("L07 M(1) tol", abs(math.exp(0.5)-1.6487213))
print("L07 cos(-2pi)", math.cos(-2*math.pi))
