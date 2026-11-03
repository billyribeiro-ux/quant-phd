"""Round 3: facts the Exemplar B memo states about the twelve Lab 3 answers, recomputed from the lab's ANSWERS."""
import ast, re
from fractions import Fraction
from pathlib import Path
src = Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-e/tests/labs/E3/lab-E3-project-3.py").read_text(encoding="utf-8")
tree = ast.parse(src)
answers = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ANSWERS":
        answers = ast.literal_eval(node.value)
print("answers:", len(answers))
prizes = [x for a in answers for x in a[2] + a[4]]
print("prize min/max (cents):", min(prizes), max(prizes))
print("prizes per lottery:", sorted({len(a[2]) for a in answers} | {len(a[4]) for a in answers}))
sums_ok = all(sum(Fraction(p) for p in a[3]) == 1 and sum(Fraction(p) for p in a[5]) == 1 for a in answers)
print("every lottery's probabilities sum to exactly 1:", sums_ok)
def mixed(prz, prb):
    return any(x > 0 and Fraction(p) > 0 for x, p in zip(prz, prb)) and any(x < 0 and Fraction(p) > 0 for x, p in zip(prz, prb))
print("pairs with a mixed lottery:", sum(1 for a in answers if mixed(a[2], a[3]) or mixed(a[4], a[5])))
print("pair 0:", answers[0])
print("pair 3:", answers[3])
print("all-gain or all-loss lotteries exist (pairs with a pure lottery):", sum(1 for a in answers if not (mixed(a[2], a[3]) and mixed(a[4], a[5]))))
