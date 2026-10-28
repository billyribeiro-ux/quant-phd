import math, sys
sys.path.insert(0, "/tmp/verifyB5-M2-e/course/modules/M/M2/grader")
from instance import make_instance
def central(f, x, h): return (f(x + h) - f(x - h)) / (2 * h)
rs = []
for s in range(50):
    x0 = make_instance(s)["x0"]
    e = lambda h: abs(central(math.sin, x0, h) - math.cos(x0))
    rs.append(e(1e-2) / e(5e-3))
print("sin central ratio min %.9f max %.9f" % (min(rs), max(rs)))
# forward ratio for cubic at seeds 0..49, both instances in grader
def cubic_prime(c, x): return c[1] + x*(2*c[2] + 3*c[3]*x)
def cubic(c, x): return c[0] + x*(c[1] + x*(c[2] + x*c[3]))
fr = []
for s in range(50):
    for seed in (s, s + 7919):
        I = make_instance(seed); c, x0 = I["cubic"], I["x0"]
        ex = cubic_prime(c, x0)
        er = lambda h: abs((cubic(c, x0 + h) - cubic(c, x0)) / h - ex)
        fr.append(er(1e-2) / er(5e-3))
print("forward ratio min %.6f max %.6f" % (min(fr), max(fr)))
