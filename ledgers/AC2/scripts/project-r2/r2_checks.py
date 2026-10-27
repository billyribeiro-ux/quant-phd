# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Round-2 project checks (AC2 project slice).

Usage (from the repository root):
    .venv/bin/python ledgers/AC2/scripts/project-r2/r2_checks.py collect 0-11
    .venv/bin/python ledgers/AC2/scripts/project-r2/r2_checks.py sample
    .venv/bin/python ledgers/AC2/scripts/project-r2/r2_checks.py lab3

collect: pytest --collect-only on the reference solution for each seed (prints the count line).
sample: 20 NEW seeds drawn with random.Random(20261028) from range(50, 1000) (disjoint from round 1's 0-49 draw);
        checks that the reference's standardize equals the generator's truth, that the answers differ, and runs the
        whole suite on the reference for each seed.
lab3: runs the modified_jones reference on the Lab 3 SAMPLE and prints the numbers the page quotes.
"""

from __future__ import annotations

import importlib.util
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "AC" / "AC2" / "grader"
SCRATCH = Path("/tmp/ac2-v/project-r2")


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def workspace(seed_candidate: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="ac2-r2-"))
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    (work / "atlas").mkdir()
    (work / "atlas" / "__init__.py").write_text("", encoding="utf-8")
    shutil.copy(seed_candidate, work / "atlas" / "fundamentals.py")
    return work


def suite(work: Path, seed: int, extra: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", "-m", "pytest", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", *extra,
         "test_project.py"],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        timeout=300,
    )


def parse(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


def collect(seeds: list[int]) -> None:
    ref = GRADER / "reference.py"
    for seed in seeds:
        work = workspace(ref)
        try:
            r = suite(work, seed, ["--collect-only", "-q"])
            m = re.search(r"(\d+) tests? collected", r.stdout) or re.search(r"(\d+) tests? collected", r.stderr)
            print(f"collect seed {seed}: {m.group(0) if m else 'NO COUNT'} rc={r.returncode}")
        finally:
            shutil.rmtree(work, ignore_errors=True)


def sample() -> None:
    inst = load("r2_instance", GRADER / "instance.py")
    seeds = sorted(random.Random(20261028).sample(range(50, 1000), 20))
    r1 = set(sorted(random.Random(20261027).sample(range(50), 20)))
    assert not (set(seeds) & r1) and not (set(seeds) & set(range(50))), "new seeds must not be round 1's"
    ref = load("r2_reference", GRADER / "reference.py")
    answers = []
    for seed in seeds:
        payload = json.loads(inst.make_instance(seed)["payload"])
        final = payload["truth"]["final"]
        latest = payload["period_ends"][-1]
        st = ref.standardize(payload["facts"])
        same = st == final
        roic = ref.roic(st, latest, 0.25)
        piot = ref.piotroski_f_score(st, latest)["score"]
        beneish = ref.beneish_m_score(st, latest)["m_score"]
        mj = ref.modified_jones(payload["sample"])
        answers.append((seed, final[latest]["revenue"], roic, piot, beneish, mj["coefficients"][1]))
        work = workspace(GRADER / "reference.py")
        try:
            r = suite(work, seed, ["-q"])
            tail = (r.stdout.strip().splitlines() or [""])[-1]
            print(f"seed {seed}: standardize==truth {same}; suite: {tail}")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print("seeds:", seeds)
    print("distinct latest revenue:", len({round(a[1], 2) for a in answers}), "of", len(answers))
    print("distinct roic:", len({round(a[2], 9) for a in answers}), "of", len(answers))
    print("distinct F:", sorted({a[3] for a in answers}))
    print("distinct M:", len({round(a[4], 9) for a in answers}), "of", len(answers))
    print("distinct mj a2:", len({round(a[5], 9) for a in answers}), "of", len(answers))


def lab3() -> None:
    ref = load("r2_reference", GRADER / "reference.py")
    rows = [
        {"total_accruals": -4.0e6, "lag_assets": 1.0e8, "d_revenue": 6.0e6, "d_receivables": 1.0e6, "ppe": 3.0e7},
        {"total_accruals": -2.5e6, "lag_assets": 8.0e7, "d_revenue": 3.0e6, "d_receivables": 0.5e6, "ppe": 2.4e7},
        {"total_accruals": -5.2e6, "lag_assets": 1.3e8, "d_revenue": 9.0e6, "d_receivables": 2.0e6, "ppe": 4.5e7},
        {"total_accruals": -1.1e6, "lag_assets": 5.0e7, "d_revenue": 1.5e6, "d_receivables": 0.2e6, "ppe": 1.1e7},
        {"total_accruals": 0.9e6, "lag_assets": 6.0e7, "d_revenue": -0.5e6, "d_receivables": 0.4e6, "ppe": 2.0e7},
        {"total_accruals": -3.3e6, "lag_assets": 9.0e7, "d_revenue": 4.0e6, "d_receivables": 1.2e6, "ppe": 3.2e7},
    ]
    out = ref.modified_jones(rows)
    print("coefficients (a1, a2, a3):", [round(c, 6) for c in out["coefficients"]])
    print("discretionary (scaled):", [round(v, 6) for v in out["discretionary"]])
    print("nondiscretionary (scaled):", [round(v, 6) for v in out["nondiscretionary"]])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "collect":
        collect(parse(sys.argv[2]))
    elif cmd == "sample":
        sample()
    elif cmd == "lab3":
        lab3()
