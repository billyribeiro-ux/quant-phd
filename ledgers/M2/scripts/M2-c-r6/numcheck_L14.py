import math, sys
sys.path.insert(0, "tests/labs/M2")
import importlib.util
spec = importlib.util.spec_from_file_location("l14", "tests/labs/M2/lab-M2-L14-1.py")
src = open("tests/labs/M2/lab-M2-L14-1.py").read().replace("\nmain()\n", "\n")
ns = {"__name__": "x"}
exec(compile(src, "lab14", "exec"), ns)
print("E1 unrounded 2exp(sin1)cos1 =", repr(2*math.exp(math.sin(1))*math.cos(1)))
print("E1 rounded factors product =", 2.3197768247*0.5403023059*2)
print("exp(sin1)", math.exp(math.sin(1)))
print("max err f1", ns["max_error"](ns["f1"], ns["f1_exact"]))
print("max err f2", ns["max_error"](ns["f2"], ns["f2_exact"]))
print("E1 val lines", ns["f1"](ns["Dual"](2.0)).val, ns["f1"](ns["Dual"](2.0,1.0)).dot, ns["f1_exact"](2.0))
print("f2' at 1", ns["f2"](ns["Dual"](1.0,1.0)).dot, ns["f2_exact"](1.0))
print("ex4.1 e^2", math.exp(2), 2*math.exp(2), 3*math.exp(2), math.sin(2), math.cos(2))
print("ex5.1 2+cos1", 2+math.cos(1), math.sin(1))
