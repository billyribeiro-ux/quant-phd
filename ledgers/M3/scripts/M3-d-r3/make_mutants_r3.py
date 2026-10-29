"""Write six verifier-authored student-error mutants (round 3, slice M3-d) from the grader's reference solution.

Each mutant is the reference covariance_doctor.py with one plausible student error applied by an exact string
replacement; every replacement must match exactly once or the script stops.
"""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path("/tmp/verifyB3-M3-d/course/modules/M/M3/grader/reference.py")
OUT = Path("/tmp/verifyB3-M3-d/ledgers/M3/mutants")

EDITS: dict[str, list[tuple[str, str]]] = {
    # is_psd uses a strict inequality: an eigenvalue exactly at -tol is refused, although the page says "at least -tol".
    "r3d_m01_is_psd_strict_at_minus_tol.py": [
        ("    return min_eigenvalue(matrix) >= -tol", "    return min_eigenvalue(matrix) > -tol"),
    ],
    # Plain alternating projections: the Dykstra correction terms are dropped, so the iterate need not be nearest.
    "r3d_m02_projection_without_dykstra_terms.py": [
        (
            "        y = _psd_projection([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])\n"
            "        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]\n"
            "        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]\n",
            "        y = _psd_projection(x)\n"
            "        corr_s = [[0.0] * n for _ in range(n)]\n"
            "        new_x = [[y[i][j] for j in range(n)] for i in range(n)]\n",
        ),
        (
            "        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]\n",
            "        corr_u = [[0.0] * n for _ in range(n)]\n",
        ),
    ],
    # comparison_weights normalises by the sum of absolute values, so the weights do not sum to one when one is negative.
    "r3d_m03_weights_normalised_by_absolute_sum.py": [
        ("    total = sum(solution)\n", "    total = sum(abs(x) for x in solution)\n"),
    ],
    # Clipping rescales by the product of the diagonals instead of the square root of it.
    "r3d_m04_clip_rescale_by_product_not_root.py": [
        (
            "    return _rescale(x)\n",
            "    d = [x[i][i] for i in range(len(x))]\n"
            "    return [[x[i][j] / (d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]\n",
        ),
    ],
    # r3d_m05 (projection returns the last PSD iterate y) was measured EQUIVALENT within the iteration tolerance
    # (survivor_witness.py: largest |y - x| 8.6e-11 over seeds 0-49), so it is not kept in the mutants list.
    # comparison_weights accepts an asymmetric correlation matrix: it skips the symmetry check the other functions run.
    "r3d_m06_weights_skip_symmetry_check.py": [
        ("    c = _as_matrix(corr)\n", "    c = [list(row) for row in corr]\n"),
    ],
}


def main() -> int:
    ref = REF.read_text(encoding="utf-8")
    for name, pairs in EDITS.items():
        text = ref
        for old, new in pairs:
            count = text.count(old)
            if count != 1:
                print(f"FAIL {name}: pattern found {count} times", file=sys.stderr)
                return 1
            text = text.replace(old, new)
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
