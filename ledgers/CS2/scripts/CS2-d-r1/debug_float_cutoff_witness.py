import sys, json
sys.path.insert(0, '/tmp/CS2-v/d/ws')
from fractions import Fraction
from streamstats import QuantileSketch
from instance import make_instance
p = json.loads(make_instance(0)['payload'])
vals = [float(x) for x in p['values']]
for L in range(1, 9):
    for eps in [0.05, 0.1, 0.2]:
        st = vals[:L]; sk = QuantileSketch(eps)
        for x in st: sk.add(x)
        for q in p['probes']:
            v = sk.quantile(q)
            below = sum(1 for x in st if x < v); le = sum(1 for x in st if x <= v)
            qn = Fraction(q) * L; sl = Fraction(eps) * L
            if not (below <= qn + sl and le >= qn - sl):
                print("L", L, "eps", eps, "q", q, "v", v, "below", below, "le", le, "qn", float(qn), "slack", float(sl))
                raise SystemExit
print("no failure in seed 0 short streams")
