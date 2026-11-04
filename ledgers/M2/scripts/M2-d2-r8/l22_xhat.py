"""L22 Part A: true location error of the golden-section maximizer against a-1, from the twin's own functions.

Imports the twin module text by exec (the twin calls main() at import, so its functions are loaded from the
source with the final line removed), then reports the exact error of x_hat, and the f_a and V' values."""
import math
from pathlib import Path

src = Path("tests/labs/M2/lab-M2-L22-1.py").read_text(encoding="utf-8")
src = src.rsplit("main()", 1)[0]
ns: dict = {}
exec(compile(src, "lab-M2-L22-1-nomain", "exec"), ns)
for a in ns["PARAMETERS_A"]:
    xs = ns["maximizer_a"](a)
    err = xs - (a - 1.0)
    print(f"a={a}: x_hat={xs!r} target={a-1.0} signed error={err:+.3e} abs={abs(err):.3e} printed x_hat={xs:.8f}")
    fa = math.log(1.0 + xs)
    print(f"   f_a(x_hat,a)-ln a = {fa - math.log(a):+.3e}")
    fx = ns["objective_a"](xs, a) - ns["objective_a"](a - 1.0, a)
    print(f"   f(x_hat)-f(a-1) = {fx:+.3e}")
print("sqrt(eps)=", math.sqrt(2.220446049250313e-16))
a = 1.5
print("0.5*0.6667*(1e-8)^2 =", 0.5 * (a / (1 + (a - 1)) ** 2) * (1e-8) ** 2)
print("f_xx at a=1.5, x=0.5:", -a / (1 + 0.5) ** 2)
