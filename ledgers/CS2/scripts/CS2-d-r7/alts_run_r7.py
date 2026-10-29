"""Round-7 verifier script: each alternative correct implementation must pass the whole suite on seeds 0-49.

Usage (from the checkout root): .venv/bin/python ledgers/CS2/scripts/CS2-d-r7/alts_run_r7.py <file> [more ...]
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402


def main() -> int:
    u = unit("CS2")
    cfg = panel(u)
    failed_any = False
    for name in sys.argv[1:]:
        source = Path(name)
        passed, failures = 0, []
        for seed in range(50):
            work = workspace(u, source, cfg)
            try:
                ok, output, _ = run_suite(work, cfg["suite"], seed)
            finally:
                shutil.rmtree(work, ignore_errors=True)
            if ok:
                passed += 1
            else:
                failures.append(seed)
        print(f"{source.name}: passes {passed}/50 seeds" + (f"; failing seeds {failures}" if failures else ""))
        failed_any = failed_any or bool(failures)
    return 1 if failed_any else 0


if __name__ == "__main__":
    sys.exit(main())
