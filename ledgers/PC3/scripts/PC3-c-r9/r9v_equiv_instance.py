"""Check that the page's draw_game (labs and project) equals grader/instance.make_instance for seeds 0..49 and extra seeds."""
import importlib.util
import random
import sys

ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location("instance", f"{ROOT}/course/modules/PC/PC3/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)


def page_draw(seed):
    # Verbatim logic of draw_game in project.html lab 1 / rung 3 (MOVE 5, thresholds 0.5, 0.25, 0.5).
    rng = random.Random(seed)
    path = [10_000]
    arrivals = []
    for _ in range(20):
        move = 5 if rng.random() < 0.5 else -5
        path.append(path[-1] + move)
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return path, arrivals


bad = []
seeds = list(range(50)) + [7919, 848197495, 1712259056, 2**31 - 1]
for s in seeds:
    p, a = page_draw(s)
    i = inst.make_instance(s)
    if p != i["fair_path_cents"] or a != i["arrivals"]:
        bad.append(s)
print("seeds checked:", len(seeds), "mismatches:", bad)
p0, a0 = page_draw(0)
print("seed0 settlement", p0[-1], "fills-free check arrivals counts", {k: a0.count(k) for k in set(a0)})
