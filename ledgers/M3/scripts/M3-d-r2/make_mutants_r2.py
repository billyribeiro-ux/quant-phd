"""Write the verifier's round-2 student-error mutants (m11-m14) into ledgers/M3/mutants/ from grader/reference.py.

Each mutant is the reference module with one plausible student error applied by exact string replacement.
The script asserts that every replacement matches exactly once, so no mutant silently equals the reference.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/M/M3/grader/reference.py"
OUT = ROOT / "ledgers/M3/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "m11_clip_ignores_floor": (
        "clip_repair ignores its floor argument and always clips at zero, so a positive floor never takes effect.",
        [("x = _rebuild([max(value, floor) for value in values], vectors)",
          "x = _rebuild([max(value, 0.0) for value in values], vectors)")],
    ),
    "m12_weights_drop_volatilities": (
        "comparison_weights uses the correlation matrix as Sigma and ignores the volatilities.",
        [("sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
          "sigma = [[c[i][j] for j in range(n)] for i in range(n)]")],
    ),
    "m13_weights_volatility_as_variance": (
        "comparison_weights treats each volatility as a variance, so Sigma is D C D with D = diag(sqrt(vol)).",
        [("sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
          "sigma = [[(float(vols[i]) ** 0.5) * c[i][j] * (float(vols[j]) ** 0.5) for j in range(n)] for i in range(n)]")],
    ),
    "m14_symmetry_relative_tolerance": (
        "_as_matrix uses a tolerance relative to the entry size, so a 5e-10 asymmetry on entries near 0.3 is refused.",
        [("if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:",
          "if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL * max(abs(out[i][j]), abs(out[j][i]), 1e-300):")],
    ),
}


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    for name, (doc, reps) in MUTANTS.items():
        text = ref
        for old, new in reps:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: pattern found {count} times: {old[:60]}")
            text = text.replace(old, new)
        text = text.replace('"""Reference solution', f'"""{doc} Student-error mutant (verifier round 2).\n\nReference solution', 1)
        # the docstring of the mutant must be its first line; the reference header follows it
        text = text.replace(f'"""{doc} Student-error mutant (verifier round 2).\n\nReference solution', f'"""{doc}\n\nMutant of the reference solution', 1)
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
