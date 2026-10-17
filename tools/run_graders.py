#!/usr/bin/env python3
"""Run a unit's autograder against its reference solution, seed by seed.

For a unit whose project is graded by ``autograder`` or ``both``:

* ``grader/instance.py`` is deterministic (same seed, same instance) and its
  instances differ across seeds
* ``grader/reference.py`` passes the whole suite on every requested seed, under
  the same pytest flags the browser uses (``--assert=plain -W error``), within
  the time limit
* the reference, the starter and the instance generator are clean under
  ``mypy --strict``
* the starter fails the suite (an empty implementation must not pass)

The solution path (for Atlas milestones, ``atlas/<module>.py``) comes from the
project page's grader panel, so the local run mirrors the browser exactly.

Usage::

    python3 tools/run_graders.py --unit S7 --seeds 0-49
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

from coursekit import ROOT, Unit, built_units, load_page, unit

PYTEST_FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
SUITE_LIMIT_S = 60.0


def panel(u: Unit) -> dict[str, str]:
    page = load_page(u.directory / "project.html")
    node = page.dom.first("section", "grader-panel")
    if node is None:
        raise SystemExit(f"{u.id}: project.html has no grader panel")
    return {k.removeprefix("data-"): v for k, v in node.attrs.items() if k.startswith("data-")}


def workspace(u: Unit, solution_source: Path, cfg: dict[str, str]) -> Path:
    grader = u.directory / cfg["grader"]
    work = Path(tempfile.mkdtemp(prefix=f"grader-{u.id}-"))
    for name in [cfg["suite"], *cfg.get("support", "").split()]:
        shutil.copy(grader / name, work / name)
    target = work / cfg["solution"]
    target.parent.mkdir(parents=True, exist_ok=True)
    for parent in target.relative_to(work).parents:
        if parent != Path():
            (work / parent / "__init__.py").touch()
    shutil.copy(solution_source, target)
    return work


def run_suite(work: Path, suite: str, seed: int) -> tuple[bool, str, float]:
    started = time.perf_counter()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *PYTEST_FLAGS, suite],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        timeout=SUITE_LIMIT_S * 5,
    )
    return result.returncode == 0, result.stdout[-2000:] + result.stderr[-2000:], time.perf_counter() - started


def check_instances(u: Unit, cfg: dict[str, str], seeds: list[int]) -> list[str]:
    path = u.directory / cfg["grader"] / "instance.py"
    spec = importlib.util.spec_from_file_location(f"instance_{u.id}", path)
    if spec is None or spec.loader is None:
        return [f"cannot load {path}"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    problems: list[str] = []

    def fingerprint(seed: int) -> str:
        inst = module.make_instance(seed)
        parts = []
        for key in sorted(inst):
            value = inst[key]
            parts.append(f"{key}={np.asarray(value).tobytes().hex()[:64] if hasattr(value, '__len__') else value}")
        return "|".join(parts)

    prints = {}
    for seed in seeds[:20]:
        first, second = fingerprint(seed), fingerprint(seed)
        if first != second:
            problems.append(f"make_instance({seed}) is not deterministic")
        prints[seed] = first
    if len(set(prints.values())) != len(prints):
        problems.append("some seeds produce identical instances")
    return problems


def typecheck(paths: list[Path]) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--ignore-missing-imports", *map(str, paths)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    return [] if result.returncode == 0 else [f"mypy --strict:\n{result.stdout.strip()}"]


def parse_seeds(text: str) -> list[int]:
    seeds: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        seeds.extend(range(int(lo), int(hi or lo) + 1))
    return seeds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true", help="every built unit with an autograder")
    parser.add_argument("--seeds", default="0-49")
    args = parser.parse_args()
    targets = built_units() if args.all else [unit(args.unit)]
    return max((grade(u, parse_seeds(args.seeds)) for u in targets), default=0)


def grade(u: Unit, seeds: list[int]) -> int:
    if u.entry["project"]["grading"] not in ("autograder", "both"):
        print(f"run_graders {u.id}: no autograder (grading: {u.entry['project']['grading']})")
        return 0
    cfg = panel(u)
    grader = u.directory / cfg["grader"]
    problems = check_instances(u, cfg, seeds)
    problems += typecheck([grader / "reference.py", grader / "instance.py", grader / cfg["starter"]])

    work = workspace(u, grader / "reference.py", cfg)
    slowest = 0.0
    passed = 0
    try:
        for seed in seeds:
            ok, output, elapsed = run_suite(work, cfg["suite"], seed)
            slowest = max(slowest, elapsed)
            if ok:
                passed += 1
            else:
                problems.append(f"reference fails on seed {seed}:\n{output}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if slowest > SUITE_LIMIT_S:
        problems.append(f"slowest local suite run took {slowest:.1f} s (limit {SUITE_LIMIT_S:.0f} s)")

    starter_work = workspace(u, grader / cfg["starter"], cfg)
    try:
        ok, _, _ = run_suite(starter_work, cfg["suite"], seeds[0])
        if ok:
            problems.append("the starter passes the suite: the tests cannot tell an empty implementation apart")
    finally:
        shutil.rmtree(starter_work, ignore_errors=True)

    for problem in problems:
        print(f"FAIL {u.id}: {problem}")
    status = "PASS" if not problems else "FAIL"
    print(f"run_graders {u.id}: {status} (reference {passed}/{len(seeds)} seeds, slowest {slowest:.1f} s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
