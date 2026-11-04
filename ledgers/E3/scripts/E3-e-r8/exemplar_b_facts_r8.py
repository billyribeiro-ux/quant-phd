"""Round-8: facts stated in exemplar B and in the Lab 3 hypothesis, read from the Lab 3 twin's ANSWERS literal.

Checks: prize range over all twelve answers; number of prizes per lottery (2 or 3); each probability list sums to exactly 1;
number of answers with a mixed-sign lottery (either lottery, positive probabilities); pair 0 and pair 3 descriptions
given in exemplar B; the answers without a mixed lottery.
Run: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/exemplar_b_facts_r8.py
"""

import ast
import pathlib
from fractions import Fraction

LAB = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e/tests/labs/E3/lab-E3-project-3.py")
tree = ast.parse(LAB.read_text(encoding="utf-8"))
answers = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "ANSWERS":
        answers = ast.literal_eval(node.value)
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "ANSWERS" for t in node.targets):
        answers = ast.literal_eval(node.value)
assert answers is not None, "ANSWERS literal not found"
print("answers:", len(answers))

all_prizes = [x for (_, _, pa, _, pb, _) in answers for x in pa + pb]
print("prize range (cents):", min(all_prizes), max(all_prizes))
counts = sorted({len(p) for (_, _, p, _, _, _) in answers} | {len(p) for (_, _, _, _, p, _) in answers})
print("prizes per lottery (distinct counts):", counts)
sums_ok = all(sum(Fraction(q) for q in qs) == 1 for (_, _, _, qs, _, _) in answers) and all(
    sum(Fraction(q) for q in qs) == 1 for (_, _, _, _, _, qs) in answers
)
print("every probability list sums to exactly 1:", sums_ok)


def mixed(prizes, probs):
    gain = any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
    loss = any(x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
    return gain and loss


mixed_ids = [a[0] for a in answers if mixed(a[2], a[3]) or mixed(a[4], a[5])]
print("answers with a mixed lottery:", len(mixed_ids), "of", len(answers), "; without:",
      [a[0] for a in answers if a[0] not in mixed_ids])
print("pair 0 A:", answers[0][2], answers[0][3], "B:", answers[0][4], answers[0][5])
print("pair 3 A:", answers[3][2], answers[3][3], "B:", answers[3][4], answers[3][5],
      "both mixed:", mixed(answers[3][2], answers[3][3]) and mixed(answers[3][4], answers[3][5]))
