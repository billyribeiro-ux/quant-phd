"""Write a validated variant of the zero-diagonal student error: validation runs first, so only the rule itself differs."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD1-M3-d")
SRC = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OLD = '    return min_eigenvalue(matrix) >= -tol\n'
NEW = (
    '    verdict = min_eigenvalue(matrix) >= -tol\n'
    '    if verdict and any(float(matrix[i][i]) == 0.0 for i in range(len(matrix))):\n'
    '        return False\n'
    '    return verdict\n'
)
assert SRC.count(OLD) == 1
body = SRC.replace(OLD, NEW, 1)
start = body.index('"""')
end = body.index('"""', start + 3) + 3
body = '"""is_psd returns False when a diagonal entry is exactly zero, although diag(0, 1, 1) is positive semidefinite."""\n' + body[end:]
(ROOT / "ledgers/M3/mutants/vd1_05_is_psd_zero_diagonal_checked_after_validation.py").write_text(body, encoding="utf-8")
print("wrote vd1_05")
