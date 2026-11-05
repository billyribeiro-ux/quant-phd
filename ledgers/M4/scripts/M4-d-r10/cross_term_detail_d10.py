"""Round-10 verifier D: per-seed cross-term relative errors for the eps probes at -0.03, +0.03, -0.05, +0.05 (seeds 0-49),
printing every seed whose error is within 0.002 of the 0.05 threshold, the failing count, and the reference's error."""

import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cross_term_d10 as ct  # noqa: E402

PROBE = HERE / "probes"
LABELS = {"ref": ct.REF, "eps+0.03": PROBE / "cross_eps_+0.03.py", "eps-0.03": PROBE / "cross_eps_-0.03.py",
          "eps+0.05": PROBE / "cross_eps_+0.05.py", "eps-0.05": PROBE / "cross_eps_-0.05.py"}


def job(args):
    label, seed = args
    return label, seed, ct.rel_error(ct.load(LABELS[label], label), seed)


if __name__ == "__main__":
    work = [(label, seed) for label in LABELS for seed in range(50)]
    with ProcessPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(job, work))
    for label in LABELS:
        errs = {s: e for lab, s, e in results if lab == label}
        failing = sorted(s for s, e in errs.items() if e > 0.05)
        near = sorted((round(e, 6), s) for s, e in errs.items() if abs(e - 0.05) < 0.002)
        print(f"{label}: failing seeds {len(failing)}/50 {failing}; near-threshold (value, seed) {near}")
    sys.stdout.flush()
