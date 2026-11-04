import ast
src = open("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/tests/labs/E3/lab-E3-project-3.py", encoding="utf-8").read()
tree = ast.parse(src)
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ANSWERS":
        A = ast.literal_eval(node.value)
print("answers", len(A))
prizes = [x for a in A for lot in (a[2], a[4]) for x in lot]
print("min prize", min(prizes), "max prize", max(prizes))
print("prize counts per lottery", sorted({len(a[2]) for a in A} | {len(a[4]) for a in A}))
mixed = lambda pr, pq: any(x > 0 and p != 0 for x, p in zip(pr, pq)) and any(x < 0 and p != 0 for x, p in zip(pr, pq))
from fractions import Fraction as F
def fr(lst): return [F(s) for s in lst]
mp = sum(1 for a in A if mixed(a[2], fr(a[3])) or mixed(a[4], fr(a[5])))
print("pairs with a mixed lottery", mp)
for a in A:
    if a[0] in (0, 3): print("pair", a[0], a[2], a[3], a[4], a[5], a[1])
# mixed per pair for claim check of lotteries with positive-probability gains and losses
for a in A:
    print(a[0], a[1], mixed(a[2], fr(a[3])), mixed(a[4], fr(a[5])))
