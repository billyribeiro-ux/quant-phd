"""Extreme inputs the page calls valid (noise volume up to 1e150, cost up to 350): reference outputs (round 13)."""
import math
import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-E4-d/course/modules/E/E4/grader")
import reference as ref

cases = [(1e150, 0.13), (1e150, 0.0), (1e150, 350.0), (1.0, 350.0), (2.0, 0.0), (1e-300, 0.13), (1e-50, 0.13), (5e-324, 0.13)]
for sd, c in cases:
    try:
        out = ref.solve_model(sd, c)
        ok = all(isinstance(v, float) and math.isfinite(v) for v in out.values())
        print(f"sd={sd:g} c={c:g}: {out} finite={ok}")
    except Exception as e:  # noqa: BLE001
        print(f"sd={sd:g} c={c:g}: raised {type(e).__name__}: {e}")
