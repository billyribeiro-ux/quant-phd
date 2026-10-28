"""Witness that the equality boundary exists in the L07 and L08 models, using the lab functions for the page's own worked case and a boundary division."""
import importlib.util
import sys
from fractions import Fraction

root = sys.argv[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    src = open(path, encoding="utf-8").read().replace("\nmain()", "\n")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


m7 = load("l07w", f"{root}/tests/labs/AC4/lab-AC4-L07-1.py")
c = m7.Case(case_id=0, v=40, p_m=60, capacity=10000, external=8000, q=5000, r_net=52)
lo, hi = m7.t_min(c), m7.t_max(c)
print("L07 worked case with r = 52: t_min", lo, "t_max", hi, "surplus", m7.firm_surplus(c), "nonempty (lo<=hi)", lo <= hi, "strict lo<hi", lo < hi)
print("L07 supplier gain at t_min", m7.supplier_increment(c, lo), "buyer gain at t_max", m7.buyer_increment(c, hi))
m8 = load("l08w", f"{root}/tests/labs/AC4/lab-AC4-L08-1.py")
d = m8.Division("BND", 100000, 9000)
ri = m8.residual_income(d)
ratio = m8.return_ratio(d)
print("L08 boundary division C=100000 OI=9000 r=9%: RI", ri, "OI/C", ratio, "RI>=0", ri >= 0, "RI>0", ri > 0, "ratio>=r", ratio >= Fraction(900, 10000), "ratio>r", ratio > Fraction(900, 10000))
