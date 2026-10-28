"""Write the verifier's student-error mutants of the M3 reference into ledgers/M3/mutants/.

Each mutant is the reference module with one edit; the edit must match exactly once or the script fails.
"""

from __future__ import annotations

from pathlib import Path

CHECKOUT = Path(__file__).resolve().parents[4]
REF = CHECKOUT / "course" / "modules" / "M" / "M3" / "grader" / "reference.py"
OUT = CHECKOUT / "ledgers" / "M3" / "mutants"

EDITS: dict[str, tuple[str, str, str]] = {
    "v01_clip_rescales_one_side.py": (
        "clip_repair rescales only the row by sqrt(d_i), so the result is not symmetric.",
        "    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]\n",
        "    return [[x[i][j] / math.sqrt(d[i]) for j in range(len(x))] for i in range(len(x))]\n",
    ),
    "v02_weights_ignore_long_vols.py": (
        "comparison_weights refuses a volatility list only when it is shorter than the matrix, so a longer one passes.",
        "    if len(vols) != n:\n",
        "    if len(vols) < n:\n",
    ),
    "v03_projection_one_pass.py": (
        "projection_repair stops after one Dykstra pass (max_iter is ignored) and returns that pass.",
        "    for _ in range(max_iter):\n        y = _psd",
        "    for _ in range(1):\n        y = _psd",
    ),
}

ASYM_EDIT = (
    "_as_matrix accepts an asymmetry up to 1e-6 instead of 1e-9, so the 1e-8 asymmetry is not refused.",
    "SYMMETRY_TOL = 1e-9",
    "SYMMETRY_TOL = 1e-6",
)


def main() -> int:
    source = REF.read_text(encoding="utf-8")
    for name, (doc, old, new) in {**EDITS, "v04_symmetry_tolerance_1e-6.py": ASYM_EDIT}.items():
        count = source.count(old)
        if count != 1:
            raise SystemExit(f"{name}: the edit matched {count} times, expected 1")
        body = source.replace(old, new, 1)
        # The docstring line of the module becomes the mutant's description; the reference's own is replaced.
        if not body.startswith('"""'):
            raise SystemExit(f"{name}: the module does not open with a docstring")
        mutant = f'"""{doc}"""\n' + body.split('"""', 2)[2].lstrip("\n")
        (OUT / name).write_text(mutant, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
