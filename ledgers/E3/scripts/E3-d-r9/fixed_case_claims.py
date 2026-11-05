# Checks the Lab 3 fixed-questionnaire claims made in project.html (Exemplar B, Rung 3 text) against the page's own data.
import re, sys
from fractions import Fraction
page = open("course/modules/E/E3/project.html", encoding="utf-8").read()
start = page.index("ANSWERS: list[tuple[int, str, list[int], list[str], list[int], list[str]]] = [")
end = page.index("\n]\n", start)
block = page[start:end]
rows = re.findall(r"\((\d+), \"([AB])\", (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\])\)", block)
print("answers parsed:", len(rows))
prizes = []
ok_counts = True
mixed_n = 0
for pid, ch, pa, qa, pb, qb in rows:
    pa, qa, pb, qb = eval(pa), eval(qa), eval(pb), eval(qb)
    prizes += pa + pb
    for pr, pq in ((pa, qa), (pb, qb)):
        if not (2 <= len(pr) <= 3 and len(pr) == len(pq)):
            ok_counts = False
        assert sum(Fraction(q) for q in pq) == 1, (pid, pq)
    def mixed(pr, pq):
        return any(x > 0 and Fraction(q) > 0 for x, q in zip(pr, pq)) and any(x < 0 and Fraction(q) > 0 for x, q in zip(pr, pq))
    mixed_n += mixed(pa, qa) or mixed(pb, qb)
print("prize min:", min(prizes), "prize max:", max(prizes))
print("every lottery has 2 or 3 prizes:", ok_counts)
print("probabilities of each lottery sum to exactly 1: True (asserted)")
print("pairs with a mixed lottery:", mixed_n)
print("pair 0:", rows[0]); print("pair 3:", rows[3])
print("pair 4 mixed (A or B):", mixed(eval(rows[4][2]), eval(rows[4][3])) or mixed(eval(rows[4][4]), eval(rows[4][5])))
