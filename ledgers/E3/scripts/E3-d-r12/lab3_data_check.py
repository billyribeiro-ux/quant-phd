"""Re-derive the Lab 3 data claims of Exemplar B (prize range, count of mixed pairs, pairs 0 and 3) from the twin.

Loads tests/labs/E3/lab-E3-project-3.py without running its main() call, then reads ANSWERS (tuples of
(pair_id, choice, prizes_a, probs_a, prizes_b, probs_b)).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8").rstrip()
assert src.endswith("main()"), "expected the twin to end with main()"
ns: dict[str, object] = {"__name__": "twin_without_main"}
exec(compile(src[: -len("main()")], "twin", "exec"), ns)
answers = ns["ANSWERS"]


def is_mixed(prizes: list[int], probs: list[str]) -> bool:
    gain = any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
    loss = any(x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
    return gain and loss


prizes: list[int] = []
mixed = 0
for _, _, pa, qa, pb, qb in answers:  # type: ignore[attr-defined]
    prizes += [*pa, *pb]
    mixed += is_mixed(pa, qa) or is_mixed(pb, qb)
print("answers", len(answers), "| min prize", min(prizes), "| max prize", max(prizes), "| mixed pairs", mixed)
print("prizes per lottery, counts:", sorted({len(p) for a in answers for p in (a[2], a[4])}))  # type: ignore[attr-defined]
for k in (0, 3):
    print(f"pair {k}:", answers[k])  # type: ignore[index]
    print(f"  mixed A {is_mixed(answers[k][2], answers[k][3])} mixed B {is_mixed(answers[k][4], answers[k][5])}")  # type: ignore[index]
