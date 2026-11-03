"""Reference answers equal to the starting portfolio over seeds 0-299; distinct answers over seeds 0-49."""
import sys, json
sys.path.insert(0, sys.argv[1])
import reference as ref
from instance import make_instance
eq = []
answers = set()
for s in range(300):
    case = json.loads(make_instance(s)["payload"])
    out = ref.allocate(case)
    if all(abs(a - b) == 0 for a, b in zip(out["weights"], case["w0"])):
        eq.append(s)
    if s < 50:
        answers.add(tuple(round(x, 12) for x in out["weights"]))
print("seeds 0-299 where the reference answer equals the starting portfolio:", eq)
print("distinct weight vectors seeds 0-49:", len(answers))
