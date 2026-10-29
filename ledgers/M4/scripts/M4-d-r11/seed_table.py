import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB11-M4-d/course/modules/M/M4/grader")
from instance import make_instance
rows = []
for s in range(50):
    i = make_instance(s)
    rows.append(f"{s}:nu{i['nu']}/n{i['n_draws']}")
print(" ".join(rows))
