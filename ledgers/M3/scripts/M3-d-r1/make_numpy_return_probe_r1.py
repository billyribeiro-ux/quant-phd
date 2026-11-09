"""Round-11 verifier probe: the reference with NumPy return types (np.bool_ verdict, ndarray matrices, np.float64 scalars).

A correct NumPy learner may return these; the grader must accept them. Written to /private/tmp/verifyD1-probe-numpy/covariance_doctor.py.
"""

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
text = REF.replace("from collections.abc import Sequence", "from collections.abc import Sequence\n\nimport numpy as np", 1)
text = text.replace(
    "    return min_eigenvalue(matrix) >= -tol",
    "    return np.bool_(min_eigenvalue(matrix) >= -tol)",
    1,
)
text = text.replace(
    "    return _rescale(x)",
    "    return np.array(_rescale(x))",
    1,
)
text = text.replace(
    "        if gap <= tol and step <= tol:\n            break\n    return x",
    "        if gap <= tol and step <= tol:\n            break\n    return np.array(x)",
    1,
)
text = text.replace("    return [x / total for x in solution]", "    return np.array([x / total for x in solution])", 1)
out = Path("/private/tmp/verifyD1-probe-numpy")
out.mkdir(parents=True, exist_ok=True)
(out / "covariance_doctor.py").write_text(text, encoding="utf-8")
print("wrote", out / "covariance_doctor.py")
