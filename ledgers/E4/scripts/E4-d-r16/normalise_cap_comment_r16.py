"""Round-16 fixer: every mutant keeps its own MAX_BISECTION_STEPS value (only the intended change may differ there) and
takes the reference's two comment lines under it. mutant_f11_01 is skipped (its intended error is the 200 cap and its
comment states that error). Usage (from the checkout root): python -I ledgers/E4/scripts/E4-d-r16/normalise_cap_comment_r16.py"""
import glob
import re
from pathlib import Path

REF = Path("course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8").splitlines()
ref_i = next(i for i, line in enumerate(REF) if line.startswith("MAX_BISECTION_STEPS = "))
REF_COMMENT = REF[ref_i + 1 : ref_i + 2]
assert all(c.startswith("# ") for c in REF_COMMENT), REF_COMMENT

changed = []
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    if Path(path).name == "mutant_f11_01_cap_200_halvings_misses_the_domain_edge.py":
        continue
    lines = Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
    idx = [i for i, line in enumerate(lines) if line.startswith("MAX_BISECTION_STEPS = ")]
    if not idx:
        continue
    i = idx[0]
    value = re.match(r"MAX_BISECTION_STEPS = (\d+)", lines[i]).group(1)
    j = i + 1
    while j < len(lines) and lines[j].startswith("# "):
        j += 1
    head = f"MAX_BISECTION_STEPS = {value}  " + REF[ref_i].split("  ", 1)[1] + "\n"
    new = [head] + [c + "\n" for c in REF_COMMENT]
    if lines[i : j] != new:
        lines[i:j] = new
        Path(path).write_text("".join(lines), encoding="utf-8")
        changed.append(Path(path).name)
print("normalised", len(changed))
