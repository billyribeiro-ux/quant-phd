"""Round-16 fixer: the 86 mutants that carry the stale cap MAX_BISECTION_STEPS = 200 (ruling-free mechanical copy
fix). Replaces the cap assignment and its continuation comment lines with the reference's block (240 and its two
comment lines). Every other line is kept, so each mutant keeps only its own intended change. mutant_f11_01 (cap 200
is its intended error) is skipped. Usage (from the checkout root): python -I ledgers/E4/scripts/E4-d-r16/regen_cap_r16.py"""
import glob
import re
from pathlib import Path

REF = Path("course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8").splitlines()
start = next(i for i, line in enumerate(REF) if line.startswith("MAX_BISECTION_STEPS = "))
end = start + 1
while end < len(REF) and REF[end].startswith("# "):
    end += 1
REF_BLOCK = REF[start:end]
assert REF_BLOCK[0].startswith("MAX_BISECTION_STEPS = 240"), REF_BLOCK

changed = []
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    if Path(path).name == "mutant_f11_01_cap_200_halvings_misses_the_domain_edge.py":
        continue
    lines = Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
    idx = [i for i, line in enumerate(lines) if line.startswith("MAX_BISECTION_STEPS = 200")]
    if not idx:
        continue
    i = idx[0]
    j = i + 1
    while j < len(lines) and lines[j].startswith("# "):
        j += 1
    new = [s + "\n" for s in REF_BLOCK]
    lines[i:j] = new
    Path(path).write_text("".join(lines), encoding="utf-8")
    changed.append(Path(path).name)
print("rewrote", len(changed))
for name in changed:
    print(name)
