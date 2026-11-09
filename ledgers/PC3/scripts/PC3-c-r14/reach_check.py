"""Which (turn, inventory) states does the reference rule reach on the fixed seeds 0-49, and what is the largest |inventory|?"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/PC/PC3/grader"))
import engine  # noqa: E402
import reference  # noqa: E402

seen = set()
maxabs = 0
minv = 0
for seed in range(50):
    def spy(state):
        seen.add((state["turn"], state["inventory"]))
        return reference.quote(state)
    log = engine.play(spy, seed)
    for t in log["turns"]:
        maxabs = max(maxabs, abs(t["inventory_after"]))
        minv = min(minv, t["inventory_after"])
print("largest |inventory_after| over seeds 0-49:", maxabs, "min inventory_after:", minv)
print("reached (turn 2-19, inventory -10):", any(t in seen for t in [(t, -10) for t in range(2, 20)]))
print("reached (turn 13, inventory 7):", (13, 7) in seen)
print("reached (turn 1 or 20, inventory -10..10) count:", sorted({i for (t, i) in seen if t in (1, 20)}))
