"""Round-11: Exemplar B's data claims (project.html Exemplar B 'Instrument' memo) against the Lab 3 twin's ANSWERS."""
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text(encoding="utf-8")
ns = {}
head = src.split("def value(")[0]
exec(compile(head, "lab3_head", "exec"), ns)
answers = ns["ANSWERS"]
prizes = [x for a in answers for x in (a[2] + a[4])]
print("prize min", min(prizes), "max", max(prizes), "prizes per lottery", sorted({len(a[2]) for a in answers}), sorted({len(a[4]) for a in answers}))
print("pair 0:", answers[0][:6])
print("pair 3:", answers[3][:6])
print("mixed pairs", sum(1 for a in answers if any(x > 0 for x in a[2]) and any(x < 0 for x in a[2]) or any(x > 0 for x in a[4]) and any(x < 0 for x in a[4])), "of", len(answers))
