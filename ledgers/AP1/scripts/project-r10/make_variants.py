import pathlib, shutil
REF = pathlib.Path("/tmp/verify-ap1-r10-m/course/modules/AP/AP1/grader")
src = (REF / "reference.py").read_text(encoding="utf-8")
head, rest = src.split("def _centred(", 1)
_, tail = rest.split("@dataclass(frozen=True)", 1)
tail = "@dataclass(frozen=True)" + tail

SEG = {
"ref": None,
# A: centred matrix + matrix_rank (relative default tolerance), lstsq solves
"a_lstsq": '''def _centred(x):
    if x.shape[0] <= x.shape[1]:
        raise ValueError("payoffs need more observations than assets for a covariance matrix")
    mu = x.mean(axis=0)
    c = x - mu
    if np.linalg.matrix_rank(c) < x.shape[1]:
        raise ValueError("the payoff covariance matrix is singular: use x_star_weights instead")
    return mu, np.asarray(c.T @ c / x.shape[0], dtype=np.float64)


def min_variance_sdf(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    beta = np.linalg.lstsq(cov, p - v * mu, rcond=None)[0]
    return v - float(mu @ beta), np.asarray(beta, dtype=np.float64)


def min_sdf_std(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    g = p - v * mu
    beta = np.linalg.lstsq(cov, g, rcond=None)[0]
    return math.sqrt(max(float(g @ beta), 0.0))


''',
# B: SVD of centred matrix with relative tolerance, pinv solves
"b_pinv": '''def _centred(x):
    if x.shape[0] <= x.shape[1]:
        raise ValueError("payoffs need more observations than assets for a covariance matrix")
    mu = x.mean(axis=0)
    c = x - mu
    s = np.linalg.svd(c, compute_uv=False)
    if s[-1] <= 1e-12 * s[0]:
        raise ValueError("the payoff covariance matrix is singular: use x_star_weights instead")
    return mu, np.asarray(c.T @ c / x.shape[0], dtype=np.float64)


def min_variance_sdf(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    beta = np.linalg.pinv(cov, rcond=1e-15) @ (p - v * mu)
    return v - float(mu @ beta), np.asarray(beta, dtype=np.float64)


def min_sdf_std(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    g = p - v * mu
    return math.sqrt(max(float(g @ np.linalg.pinv(cov, rcond=1e-15) @ g), 0.0))


''',
# C: np.cov(bias=True), relative condition-number guard, np.linalg.solve
"c_cov_solve": '''def _centred(x):
    if x.shape[0] <= x.shape[1]:
        raise ValueError("payoffs need more observations than assets for a covariance matrix")
    mu = np.mean(x, axis=0)
    cov = np.cov(x, rowvar=False, bias=True)
    if not np.isfinite(np.linalg.cond(cov)) or np.linalg.cond(cov) > 1e13:
        raise ValueError("the payoff covariance matrix is singular: use x_star_weights instead")
    return mu, np.asarray(cov, dtype=np.float64)


def min_variance_sdf(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    beta = np.linalg.solve(cov, p - v * mu)
    return v - float(np.dot(mu, beta)), np.asarray(beta, dtype=np.float64)


def min_sdf_std(payoffs, prices, mean):
    x = _matrix(payoffs, "payoffs")
    p = _vector(prices, "prices", x.shape[1])
    v = float(mean)
    if not math.isfinite(v):
        raise ValueError("mean must be finite")
    mu, cov = _centred(x)
    g = p - v * mu
    return math.sqrt(max(float(np.dot(g, np.linalg.solve(cov, g))), 0.0))


''',
}
for name, seg in SEG.items():
    d = pathlib.Path(f"/tmp/ap1-r5/project-r10/{name}")
    d.mkdir(parents=True, exist_ok=True)
    for f in ("test_project.py", "instance.py"):
        shutil.copy(REF / f, d / f)
    if seg is None:
        body = src
    else:
        body = head + seg + tail
    (d / "sdf_recovery.py").write_text(body, encoding="utf-8")
    print(name, "written", len(body))
