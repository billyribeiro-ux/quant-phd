"""Write round-4 student-error mutants of the M5 reference into ledgers/M5/mutants/ (slice d, round 4).

Each mutant is the reference with one edit. Its first docstring line names the student error. None sits at a
tolerance boundary (ruling 25): each changes a behaviour the page states.
"""
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
REF = (REPO / "course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
OUT = REPO / "ledgers/M5/mutants"

MUTANTS = {
    "r4_01_change_is_the_euclidean_norm_of_the_difference.py": (
        "Student-error mutant (M5 slice d round 4): the change of a sweep is the Euclidean norm of the difference, "
        "not the largest absolute entry, so the certified error is computed from the wrong norm.",
        "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))",
        "        change = math.sqrt(sum((a - b) ** 2 for a, b in zip(new, values, strict=True)))",
    ),
    "r4_02_certificate_factor_is_one_minus_beta_over_beta.py": (
        "Student-error mutant (M5 slice d round 4): the certified error uses (1 - beta) / beta in place of "
        "beta / (1 - beta), inverting the geometric-sum factor of the certified bound.",
        "    factor = beta / (1 - beta)\n    values = [0.0] * len(points)",
        "    factor = (1 - beta) / beta\n    values = [0.0] * len(points)",
    ),
    "r4_03_continuation_reads_the_next_grid_value.py": (
        "Student-error mutant (M5 slice d round 4): the continuation term uses V at the grid point after the saving, "
        "an index off by one, instead of V(k') at the saving itself.",
        "                best = max(best, math.sqrt(available - successor) + beta * continuation)",
        "                best = max(best, math.sqrt(available - successor) + beta * continuation)\n"
        "        best = best  # placeholder",
    ),
    "r4_04_utility_takes_the_root_of_the_output_only.py": (
        "Student-error mutant (M5 slice d round 4): the utility is the square root of the output alone minus the "
        "saving, a parenthesis error that writes sqrt(k**alpha) - k' in place of sqrt(k**alpha - k').",
        "                best = max(best, math.sqrt(available - successor) + beta * continuation)",
        "                best = max(best, math.sqrt(available) - successor + beta * continuation)",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    if name.startswith("r4_03"):
        # The index error is written in full below; the placeholder above is replaced by the explicit version.
        continue
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1)
    lines = text.split("\n")
    end = text.index('"""', 3) + 3
    body = text[end:]
    text = f'"""{doc}"""' + body
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)

# r4_03: the continuation term reads the next grid value, clipped at the top point.
old_sweep = "        for successor, continuation in zip(grid, values, strict=True):\n            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)"
assert REF.count(old_sweep) == 1
new_sweep = (
    "        for j, successor in enumerate(grid):\n            if successor <= available:\n"
    "                continuation = values[min(j + 1, len(values) - 1)]\n"
    "                best = max(best, math.sqrt(available - successor) + beta * continuation)"
)
name = "r4_03_continuation_reads_the_next_grid_value.py"
text = REF.replace(old_sweep, new_sweep, 1)
doc = MUTANTS[name][0]
text = f'"""{doc}"""' + text[text.index('"""', 3) + 3 :]
(OUT / name).write_text(text, encoding="utf-8")
print("wrote", name)
