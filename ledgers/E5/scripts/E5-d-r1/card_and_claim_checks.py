# Verifier E5-d round 1 scratch checks (run with the checkout's .venv under python -I -W error)
import math, sys
from fractions import Fraction
import importlib.util
# card numbers
print("1.1^0.3 =", round(1.1**0.3, 6), "simple", round(1.1**0.3 - 1, 6), "0.3 ln1.1 =", round(0.3*math.log(1.1), 6))
print("ln1.25 =", round(math.log(1.25), 6), "0.25 - ln1.25 =", round(0.25 - math.log(1.25), 6))
print("real growth exact =", round((1100/995)/(27/23) - 1, 6), "nominal", round(105/995, 6), "deflator", round(4/23, 6))
print("x-ln(1+x):", [round(x - math.log(1+x), 6) for x in (0.01, 0.05, 0.25)])
print("basket A gap", Fraction(5,4) - Fraction(27,23))
print("k*", (0.2/0.06)**(1/0.7), "y*", (0.2/0.06)**(0.3/0.7)**1 if False else (0.2/0.06)**(0.3/0.7))
print("Bernoulli c^N <= 1/(1+N(1/c-1)) at c=0.6:", [(0.6**N <= 1/(1+N*(1/0.6-1))+1e-15) for N in range(1, 40)].count(False) == 0)
# ranking claim counterexample (L07 section 1 says the sign and ranking are unchanged by the change of units)
Y1, T1, Y2, T2 = 110.0, 100.0, 1020.0, 1000.0
print("level gaps", Y1-T1, Y2-T2, "pct gaps", 100*(Y1-T1)/T1, 100*(Y2-T2)/T2)
# discount vs yield for a 91-day bill at price 98 per 100 face
F, P, t = 100.0, 98.0, 91
d = (F-P)/F*360/t; y = (F-P)/P*365/t
print("discount", round(d, 6), "yield", round(y, 6), "discount below yield:", d < y)
# Lab 3 spread reader on a blank value (docstring says days where both yields are published)
try:
    Fraction("") 
except ValueError as e:
    print("blank cmt raises ValueError:", e)
# Lab 2 simulated spread
spec = importlib.util.spec_from_file_location("p2", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
path = m.simulated_path(); yl = m.simulated_yields(path["policy"]); t = m.QUARTERS - 1
print("lab2 spread", yl["cmt_10y"][t] - yl["tbill_3m"][t])
