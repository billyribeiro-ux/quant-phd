"""Generate round-8 student-error mutants of the M3 reference solution (verifier-authored, not shipped)."""

import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M3-d")
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"


def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (src.count(old), old[:80])
    return src.replace(old, new)


def body_block(src: str, name: str, new_body: str) -> str:
    pattern = re.compile(rf"def {name}\(.*?(?=\ndef )", re.S)
    m = pattern.search(src)
    assert m is not None
    head = m.group(0).split("\n", 1)[0]
    return src[: m.start()] + head + "\n" + new_body + src[m.end() :]


MUTANTS = {}

MUTANTS["r8d_m01_weights_refuse_only_exact_zero.py"] = (
    "comparison_weights refuses only an exactly zero volatility, so a negative volatility is accepted.",
    swap(REF, "if any(float(v) <= 0.0 for v in vols):", "if any(float(v) == 0.0 for v in vols):"),
)

MUTANTS["r8d_m02_projection_three_passes.py"] = (
    "projection_repair stops after three Dykstra passes whatever tol and max_iter are.",
    swap(REF, "    for _ in range(max_iter):\n        y = _psd_projection", "    for _ in range(3):\n        y = _psd_projection"),
)

MUTANTS["r8d_m03_weights_sigma_variance_on_rows.py"] = (
    "comparison_weights builds Sigma_ij = v_i^2 C_ij (variance on the row only), which is neither symmetric nor S C S.",
    swap(
        REF,
        "sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
        "sigma = [[float(vols[i]) ** 2 * c[i][j] for j in range(n)] for i in range(n)]",
    ),
)

MUTANTS["r8d_m04_is_psd_checks_diagonal_only.py"] = (
    "is_psd tests the diagonal entries against -tol instead of the eigenvalues.",
    body_block(
        REF,
        "is_psd",
        '    """True when every eigenvalue of the symmetric matrix is at least -tol."""\n'
        "    return all(float(matrix[i][i]) >= -tol for i in range(len(matrix)))\n\n",
    ),
)

MUTANTS["r8d_m05_projection_one_shot_pin.py"] = (
    "projection_repair takes the eigenvalue clipping of the input and sets its diagonal to 1 without rescaling.",
    body_block(
        REF,
        "projection_repair",
        "    n = len(matrix)\n"
        "    y = _psd_projection(_as_matrix(matrix))\n"
        "    for i in range(n):\n"
        "        y[i][i] = 1.0\n"
        "    return y\n\n",
    ),
)

for name, (doc, src) in MUTANTS.items():
    text = f'"""{doc}"""\n' + src.split('"""', 2)[2]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
