import sys, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB11-M3-d/course/modules/M/M3/grader")
import reference as r
for vols in ([float("nan"), 0.2], [0.1, float("nan")], [0.1, float("inf")]):
    try:
        print("vols", vols, "->", r.comparison_weights([[1.0, 0.3], [0.3, 1.0]], vols))
    except ValueError as e:
        print("vols", vols, "-> ValueError", e)
