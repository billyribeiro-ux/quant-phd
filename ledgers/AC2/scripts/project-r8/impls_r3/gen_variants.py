from pathlib import Path
T = Path("/tmp/ac2-v/project/cands/template.py").read_text()

NORM = '''def _norm_cols(design):
    norms = np.linalg.norm(design, axis=0)
    if np.any(norms == 0.0):
        raise ValueError("rank-deficient: a regressor is identically zero")
    return design / norms
'''

def svd_rank(rel):
    return NORM + f'''

def _rank_check(design):
    x = _norm_cols(design)
    s = np.linalg.svd(x, compute_uv=False)
    if s[-1] <= {rel!r} * s[0]:
        raise ValueError("rank-deficient design")
'''

COND = NORM + '''

def _rank_check(design):
    x = _norm_cols(design)
    if not np.linalg.cond(x) <= 1e12:
        raise ValueError("rank-deficient design (condition number above 1e12)")
'''

CHOL = NORM + '''

def _rank_check(design):
    x = _norm_cols(design)
    gram = x.T @ x
    try:
        factor = np.linalg.cholesky(gram)
    except np.linalg.LinAlgError:
        raise ValueError("rank-deficient design (Cholesky failed)") from None
    if float(np.min(np.diag(factor))) ** 2 <= 1e-10:
        raise ValueError("rank-deficient design (pivot below tolerance)")
'''

STRICT_VAL = '''
def _is_bool_like(value):
    return isinstance(value, (bool, np.bool_))
'''
STRICT_NUM = '''def _num(value: Any, what: str) -> float:
    if _is_bool_like(value):
        raise ValueError(f"{what} must be a number, not a bool")
    if not isinstance(value, Real) or not math.isfinite(float(value)):
        raise ValueError(f"{what} must be a finite number")
    return float(value)
'''
BASE_NUM_OLD = '''def _num(value: Any, what: str) -> float:
    if not isinstance(value, Real) or not math.isfinite(float(value)):
        raise ValueError(f"{what} must be a finite number")
    return float(value)
'''
assert T.count(BASE_NUM_OLD) == 1

variants = {
    "V1_svd_1e-8": (svd_rank(1e-8), ""),
    "V2_svd_1e-12": (svd_rank(1e-12), ""),
    "V3_condition_1e12": (COND, ""),
    "V4_cholesky_pivot": (CHOL, ""),
    "V5_strict_bool_rejecting_svd_1e-10": (svd_rank(1e-10), STRICT_VAL),
}
for name, (rank, val) in variants.items():
    src = T.replace("__VARIANT__", name).replace("#RANK#", rank)
    if val:
        src = src.replace(BASE_NUM_OLD, STRICT_NUM).replace("#VALIDATION#", val)
    else:
        src = src.replace(BASE_NUM_OLD, BASE_NUM_OLD).replace("#VALIDATION#", "")
    assert "#RANK#" not in src and "#VALIDATION#" not in src
    out = Path(f"/tmp/ac2-v/project/cands/{name}.py")
    out.write_text(src)
    print("wrote", out)
