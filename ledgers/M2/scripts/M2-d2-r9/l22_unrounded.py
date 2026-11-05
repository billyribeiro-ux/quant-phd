import sys, math
sys.path.insert(0, "/tmp/m2d2r9_L22")
import importlib.util
spec = importlib.util.spec_from_file_location("twin", "/Users/billyribeiro/.fanout/wt/verifyD9-M2-d2/tests/labs/M2/lab-M2-L22-1.py")
src = open(spec.origin).read().replace("\nmain()", "\n")
ns = {"__name__": "x"}
exec(compile(src, "twin_noMain", "exec"), ns)
for a in ns["PARAMETERS_A"]:
    xh = ns["maximizer_a"](a)
    print("A a=%r xhat=%.17g exact=%.17g err=%.6e (err/1e-8=%.4f) fa=%.17g ln=%.17g fa-ln=%.3e" % (
        a, xh, a-1, xh-(a-1), (xh-(a-1))/1e-8, math.log(1+xh), math.log(a), math.log(1+xh)-math.log(a)))
for a in ns["PARAMETERS_B"]:
    xh = ns["maximizer_b"](a)
    print("B a=%r xhat=%.17g exact=%.17g err=%.6e" % (a, xh, a/2, xh-a/2))
# theory check: f_xx at xhat for a=1.5
a=1.5; xh=ns["maximizer_a"](a)
print("fxx", -a/(1+xh)**2, "half*fxx*1e-16", 0.5*abs(-a/(1+xh)**2)*1e-16)
# exact central diff of V at a=1.5 with exact V
V=lambda a: a*math.log(a)-(a-1)
print("exact central diff check", (V(1.5+1e-4)-V(1.5-1e-4))/(2e-4), math.log(1.5))
