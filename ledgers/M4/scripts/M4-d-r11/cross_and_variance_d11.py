"""Round-11 verifier d: (1) the cross-term probes over seeds 0-49 (the test's statistic, 100,000 draws, nu = 5, relative
error against 4 w1 w2 Sigma_12, threshold 0.05), with the factor entry L[1][0] scaled by (1 + eps); (2) the Student-t
variance check over seeds 0-1999 for the reference and for the missing-factor probe (matched factor replaced by 1).
Usage: python cross_and_variance_d11.py <checkout-root> <cross|variance|all>"""

import importlib.util
import math
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
MODE = sys.argv[2] if len(sys.argv) > 2 else "all"
REF = ROOT / "course/modules/M/M4/grader/reference.py"
SCR = Path(tempfile.mkdtemp(prefix="m4d11probe"))
sys.path.insert(0, str(ROOT / "course/modules/M/M4/grader"))
import instance as inst  # noqa: E402

TEXT = REF.read_text(encoding="utf-8")
OLD = "    return factor\n"
assert TEXT.count(OLD) == 1
EPS = [0.0, 0.03, -0.03, 0.05, -0.05]
MISS_OLD = "    matched = matched_scale(nu) if student and nu is not None else 1.0\n"
assert TEXT.count(MISS_OLD) == 1


def write_probe(name: str, text: str) -> Path:
    path = SCR / f"{name}.py"
    path.write_text(text, encoding="utf-8")
    return path


PROBES = {}
for e in EPS:
    text = TEXT.replace(
        OLD, f"    if len(factor) == 2:\n        factor[1][0] *= {1.0 + e!r}\n" + OLD
    )
    PROBES[f"eps{e:+.2f}"] = write_probe(f"cross_eps_{e:+.2f}".replace("+", "p").replace("-", "m").replace(".", "_"), text)
PROBES["missing_factor"] = write_probe("missing_factor", TEXT.replace(MISS_OLD, "    matched = 1.0\n"))
PROBES["ref"] = REF


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fsum_var(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def cross_error(args):
    label, seed = args
    mod = load(PROBES[label], "m_" + label.replace("+", "p").replace("-", "m").replace(".", "_"))
    w1, w2 = 1_000_000, 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = mod.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
    minus = mod.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    return label, seed, abs((fsum_var(plus) - fsum_var(minus)) / target - 1.0)


def variance_error(args):
    label, seed = args
    i = inst.make_instance(seed)
    pos, cov, nu, n = i["positions_cents"], i["cov"], i["nu"], i["n_draws"]
    target = math.fsum(pos[a] * pos[b] * cov[a][b] for a in range(len(pos)) for b in range(len(pos)))
    mod = load(PROBES[label], "v_" + label)
    losses = mod.simulate_losses(pos, cov, n, seed, "student_t", nu)
    return label, seed, nu, abs(fsum_var(losses) / target - 1.0)


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=12) as ex:
        if MODE in ("cross", "all"):
            work = [(lab, s) for lab in [f"eps{e:+.2f}" for e in EPS] for s in range(50)]
            rows = list(ex.map(cross_error, work, chunksize=5))
            for e in EPS:
                lab = f"eps{e:+.2f}"
                errs = {s: x for l, s, x in rows if l == lab}
                failing = sorted(s for s, x in errs.items() if x > 0.05)
                print(f"cross {lab}: failing seeds {len(failing)}/50 {failing}; max error {max(errs.values()):.4f}; "
                      f"min error {min(errs.values()):.4f}")
            sys.stdout.flush()
        if MODE in ("variance", "all"):
            work = [(lab, s) for lab in ("ref", "missing_factor") for s in range(2000)]
            rows = list(ex.map(variance_error, work, chunksize=20))
            ref_1093 = [r[3] for r in rows if r[0] == "ref" and r[1] == 1093]
            print("reference relative variance error at seed 1093:", [round(x, 4) for x in ref_1093])
            for nu in range(3, 9):
                ref_sel = [r for r in rows if r[0] == "ref" and r[2] == nu]
                miss_sel = [r for r in rows if r[0] == "missing_factor" and r[2] == nu]
                print(f"variance nu {nu}: seeds {len(ref_sel)}; reference max {max(r[3] for r in ref_sel):.4f}; "
                      f"reference over 0.30: {sum(r[3] > 0.30 for r in ref_sel)}; "
                      f"missing-factor over 0.30: {sum(r[3] > 0.30 for r in miss_sel)} of {len(miss_sel)}")
            sys.stdout.flush()
