"""Round-7 verifier script: list EVERY failing test for each grader mutant, not only the first.

tools/mutate_graders.py attributes a kill to the first FAILED line in pytest's output, which is the first
failing test in file order and can name a test unrelated to the mutant's described error. This script runs
the same suite (same workspace construction and pytest flags as tools/run_graders.py) and records all
failing test ids per mutant and seed.

Usage (from the checkout root):
    .venv/bin/python ledgers/CS2/scripts/CS2-d-r7/killers_r7.py <mutant-dir-or-file> [more ...] --seeds 0-9
"""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, workspace  # noqa: E402
import subprocess  # noqa: E402
import os  # noqa: E402
from run_graders import PYTEST_FLAGS  # noqa: E402


def failing(work: Path, suite: str, seed: int) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *PYTEST_FLAGS, "-rf", suite],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        timeout=600,
    )
    return sorted(set(re.findall(r"^FAILED \S+::(\S+)", result.stdout, flags=re.M)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--seeds", default="0-9")
    args = parser.parse_args()
    u = unit("CS2")
    cfg = panel(u)
    files: list[Path] = []
    for p in args.paths:
        path = Path(p)
        files.extend(sorted(path.glob("*.py")) if path.is_dir() else [path])
    seeds = parse_seeds(args.seeds)
    survivors = 0
    for mutant in files:
        description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
        per_seed: dict[int, list[str]] = {}
        for seed in seeds:
            work = workspace(u, mutant, cfg)
            try:
                per_seed[seed] = failing(work, cfg["suite"], seed)
            finally:
                shutil.rmtree(work, ignore_errors=True)
        union = sorted({t for names in per_seed.values() for t in names})
        survivors += not union
        seed0 = per_seed.get(seeds[0], [])
        print(
            f"{'KILLED' if union else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]}\n"
            f"    failing on seed {seeds[0]} ({len(seed0)}): {', '.join(seed0[:6])}{' ...' if len(seed0) > 6 else ''}\n"
            f"    union over seeds {seeds[0]}..{seeds[-1]}: {len(union)} distinct tests"
        )
    print(f"killers_r7: {len(files) - survivors}/{len(files)} killed")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
