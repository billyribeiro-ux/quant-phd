"""Round-10 verifier D: the cross-term error probes built the other way: the covariance input's off-diagonal entry is scaled
by (1 + eps) before the Cholesky factor is computed (instead of scaling the factor's [1][0] entry). Same statistic and
threshold as the test (100,000 draws, nu = 5, seeds 0-49). Prints failing-seed counts per eps."""

import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cross_term_d10 as ct  # noqa: E402

EPS_LIST = [0.0, 0.03, -0.03, 0.05, -0.05]


def make(eps: float, label: str):
    text = ct.REF.read_text(encoding="utf-8")
    old = "    factor = _cholesky(cov, n)\n"
    assert text.count(old) == 1, "reference must compute the factor from cov once"
    new = (
        "    if n == 2:\n"
        f"        cov = [[cov[0][0], cov[0][1] * {1.0 + eps!r}], [cov[1][0] * {1.0 + eps!r}, cov[1][1]]]\n"
        "    factor = _cholesky(cov, n)\n"
    )
    path = HERE / "probes" / f"covinput_{label}.py"
    path.write_text(text.replace(old, new), encoding="utf-8")
    return path


def job(args):
    label, path, seed = args
    return label, seed, ct.rel_error(ct.load(path, label), seed)


if __name__ == "__main__":
    paths = {}
    for eps in EPS_LIST:
        label = f"eps{eps:+.2f}"
        paths[label] = make(eps, label.replace("+", "p").replace("-", "m").replace(".", "_"))
    work = [(label, path, seed) for label, path in paths.items() for seed in range(50)]
    with ProcessPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(job, work))
    for label in paths:
        errs = {s: e for lab, s, e in results if lab == label}
        failing = sorted(s for s, e in errs.items() if e > 0.05)
        print(f"covinput {label}: failing seeds {len(failing)}/50 {failing}; max error {max(errs.values()):.4f}")
    sys.stdout.flush()
