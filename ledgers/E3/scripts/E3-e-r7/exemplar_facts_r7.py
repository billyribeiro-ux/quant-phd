"""Facts that exemplar B and the Lab 3 description state, recomputed from the Lab 3 twin's ANSWERS literal."""
import re
import sys
from fractions import Fraction
from pathlib import Path

twin = (Path(sys.argv[1]) / "tests/labs/E3/lab-E3-project-3.py").read_text(encoding="utf-8")
block = re.search(r"ANSWERS: list\[.*?\n\]\n", twin, re.S).group(0)
ns: dict[str, object] = {}
exec(block, {}, ns)
answers = ns["ANSWERS"]
prizes = [x for a in answers for x in a[2] + a[4]]
print("answers:", len(answers), "| min prize:", min(prizes), "| max prize:", max(prizes))
print("prizes per lottery:", sorted({len(a[2]) for a in answers} | {len(a[4]) for a in answers}))
sums_ok = all(sum(Fraction(p) for p in a[3]) == 1 and sum(Fraction(p) for p in a[5]) == 1 for a in answers)
print("every lottery's probabilities sum to exactly 1:", sums_ok)


def mixes(prizes: list[int], probs: list[str]) -> bool:
    return any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True)) and any(
        x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True)
    )


flags = [mixes(a[2], a[3]) or mixes(a[4], a[5]) for a in answers]
print("pairs with a mixed lottery:", sum(flags), [i for i, f in enumerate(flags) if not f], "(indices without)")
print("pair 0:", answers[0])
print("pair 3:", answers[3])
