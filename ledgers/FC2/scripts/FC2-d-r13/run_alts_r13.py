"""Run every correct alternative implementation of FC2 against the suite, seed by seed (scratch, round 13)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
sys.path.insert(0, str(ROOT / "tools"))

from run_graders import PYTEST_FLAGS, panel, run_suite, workspace  # noqa: E402
from coursekit import unit  # noqa: E402

ALT_DIRS = [
    ROOT / "ledgers/FC2/scripts/FC2-d-r10/alts",
    ROOT / "ledgers/FC2/scripts/FC2-d-r11/alts",
]


def main() -> int:
    u = unit("FC2")
    cfg = panel(u)
    alts = sorted(p for d in ALT_DIRS for p in d.glob("alt*.py"))
    failures = 0
    for alt in alts:
        bad = []
        for seed in range(50):
            work = workspace(u, alt, cfg)
            try:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
            finally:
                import shutil

                shutil.rmtree(work, ignore_errors=True)
            if not ok:
                bad.append(seed)
                first = output.strip().splitlines()[-1:] or [""]
                print(f"  {alt.name} seed {seed}: {first[0]}")
                break
        status = "PASS" if not bad else "FAIL"
        failures += bool(bad)
        print(f"{alt.name}: {status} {50 - len(bad)}/50 seeds")
    print(f"alts: {len(alts)} files, {len(alts) - failures} pass, {failures} fail")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
