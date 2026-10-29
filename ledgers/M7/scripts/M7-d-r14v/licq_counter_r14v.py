import sys, json
sys.path.insert(0, "/tmp/m7d_r14_collect")
import constrained_allocator as sol
case = {
    "gamma": 2, "mu": [0.1, 0.1, 0.1],
    "sigma": [[0.5, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 0.5]],
    "w0": [0.2, 0.3, 0.5], "lower": [0.0, 0.0, 0.0], "upper": [0.2, 0.3, 0.5],
    "sector": [0, 0, 1], "sector_caps": [1.0, 1.0], "turnover_limit": 1.0,
}
out = sol.allocate(case)
print(json.dumps(out, default=str, sort_keys=True)[:3000])
