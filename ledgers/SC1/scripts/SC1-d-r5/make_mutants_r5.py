"""Verifier r5 (SC1-d): three new student-error mutants, each a single-change copy of grader/reference.py.

Each replacement must match exactly once, or the script stops. Output: ledgers/SC1/mutants/m32..m34.
"""
from pathlib import Path
import sys

ROOT = Path(sys.argv[1])
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"

CHANGES = {
    "m32_coarse_stride_taken_as_n_coarse.py": (
        "Coarse grid stride uses n_coarse instead of n_fine / n_coarse, so the coarse grid has the wrong points.",
        "    stride = n_fine // n_coarse\n",
        "    stride = n_coarse\n",
    ),
    "m33_srw_max_doubles_terminal_count.py": (
        "srw_max_count returns twice the terminal count at a, instead of the reflection identity.",
        "    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
        "    return 2 * srw_terminal_count(n, a)",
    ),
    "m34_step_sd_divided_by_steps.py": (
        "Gaussian step sd is sqrt(H) / n_steps instead of sqrt(H / n_steps), so the grid law is wrong for n > 1.",
        "    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n",
        "    sd = math.sqrt(float(instance[\"H\"])) / n_steps\n",
    ),
}

for name, (doc, old, new) in CHANGES.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    # one-line docstring describing the error, as the mutate tool expects
    end = body.index('"""', 3) + 3  # the module docstring of reference.py spans several lines
    body = f'"""Mutant: {doc}"""' + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
