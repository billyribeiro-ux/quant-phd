"""Writes the verifier's round-2 student-error mutants (n01 to n04) from the reference solution.

Each mutant is the reference module with one plausible student error applied; every replacement must match exactly
once in the reference. Run from the checkout:  python3 ledgers/M4/scripts/M4-d-r2/make_mutants_r2.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

# name -> (what the student error is, [(old, new), ...])
EDITS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "n01_matched_factor_not_square_rooted.py": (
        "The matched factor enters the Student-t scale without its square root: scale = matched * sqrt(nu / W).",
        [
            (
                "            scale = math.sqrt(matched * nu / chi_square)",
                "            scale = matched * math.sqrt(nu / chi_square)",
            )
        ],
    ),
    "n02_one_chi_square_per_asset.py": (
        "The Student-t draws one chi-square variable per asset instead of one per draw, so assets do not share a scale.",
        [
            (
                "        scale = 1.0\n"
                "        if student and nu is not None:\n"
                "            chi_square = rng.gammavariate(nu / 2, 2.0)\n"
                "            scale = math.sqrt(matched * nu / chi_square)\n"
                "        total = 0.0\n"
                "        for i in range(n):\n"
                "            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))",
                "        total = 0.0\n"
                "        for i in range(n):\n"
                "            scale = 1.0\n"
                "            if student and nu is not None:\n"
                "                chi_square = rng.gammavariate(nu / 2, 2.0)\n"
                "                scale = math.sqrt(matched * nu / chi_square)\n"
                "            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))",
            )
        ],
    ),
    "n03_transposed_factor.py": (
        "The returns use the transpose of the Cholesky factor, so the simulated covariance is L^T L, not L L^T.",
        [
            (
                "            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))",
                "            ret = scale * sum(factor[k][i] * z[k] for k in range(i, n))",
            )
        ],
    ),
    "n04_student_t_chi_square_nu_minus_one.py": (
        "The chi-square of the Student-t draw has nu - 1 degrees of freedom: shape (nu - 1) / 2.",
        [("            chi_square = rng.gammavariate(nu / 2, 2.0)", "            chi_square = rng.gammavariate((nu - 1) / 2, 2.0)")],
    ),
}

for name, (doc, pairs) in EDITS.items():
    text = REF
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"{name}: expected one match, found {count}")
        text = text.replace(old, new)
    (OUT / name).write_text(f"# Verifier round-2 student-error mutant. {doc}\n" + text, encoding="utf-8")
    print("wrote", name)
