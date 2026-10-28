import sys
sys.path.insert(0, "/tmp/verify12-CF1-d/course/modules/CF/CF1/grader")
import reference as r
from math import isclose
flows = [-9000.0, 3150.0, 4000.0, 5000.0]
print("npv10", round(r.npv(0.10, flows), 2))
print("irr roots", r.irr_roots(flows))
print("npv at irr", r.npv(0.153177, flows))
print("zero flow npv", r.npv(0.1, [-100.0, 0.0, 121.0]), r.npv(0.1, [0.0, 121.0]))
print("payback", r.payback_period(flows), r.payback_period(flows, 0.10))
print("1-d sweep sign changes:", sum(1 for a,b in zip([r.npv(x/1000, flows) for x in range(-900,3000)],[r.npv(x/1000,flows) for x in range(-899,3001)]) if a*b<0))
print("shield pv", sum(750*0.25/(1.1**t) for t in range(1,4)))
