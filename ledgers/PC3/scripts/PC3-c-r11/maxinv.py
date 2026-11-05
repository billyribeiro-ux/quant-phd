import sys
sys.path.insert(0, sys.argv[1])
import reference, engine
best = {}
for seed in list(range(50)) + [848197495, 1712259056]:
    log = engine.play(reference.quote, seed)
    inv = [t["inventory_after"] for t in log["turns"]]
    best[seed] = max(abs(x) for x in inv)
print("max |inventory| over seeds 0-49:", max(best[s] for s in range(50)), "seeds reaching 10:", [s for s in range(50) if best[s] >= 10])
print("max |inventory| on learner-style seeds 848197495, 1712259056:", best[848197495], best[1712259056])
print("count of seeds 0-49 with max |inventory| == 9:", sum(1 for s in range(50) if best[s] == 9))
