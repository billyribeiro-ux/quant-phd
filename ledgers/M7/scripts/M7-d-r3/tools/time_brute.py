import json, sys, time
sys.path.insert(0, sys.argv[1])
from instance import make_instance
import constrained_allocator as alt
seeds = [s for s in range(50) if len(json.loads(make_instance(s)["payload"])["mu"]) == 5][:2]
for s in seeds:
    case = json.loads(make_instance(s)["payload"])
    t = time.time()
    out = alt.allocate(case)
    print("seed", s, "n=5 allocate seconds", round(time.time() - t, 2), "cert", {k: f"{v:.1e}" for k, v in out["certificate"].items()})
