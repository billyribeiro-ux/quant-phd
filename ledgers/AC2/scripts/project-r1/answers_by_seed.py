# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Print the graded answers of the reference solution for the 20 sampled seeds (AC2 project).

Usage (from the repository root): .venv/bin/python ledgers/AC2/scripts/project-r1/answers_by_seed.py

Imports the course's reference.py and instance.py by path (read-only) and prints, per seed: the latest revenue,
the ROIC at 25% tax, the Piotroski score, the Beneish M-score, the modified Jones a2 and the discretionary accrual of
firm-year 0. The point is that the numbers change with the seed, not only the labels.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "AC" / "AC2" / "grader"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ref = load("ac2_reference", GRADER / "reference.py")
    inst = load("ac2_instance", GRADER / "instance.py")
    seeds = sorted(random.Random(20261027).sample(range(50), 20))
    rows = []
    for seed in seeds:
        payload = json.loads(inst.make_instance(seed)["payload"])
        final = payload["truth"]["final"]
        ends = payload["period_ends"]
        latest, prev = ends[-1], ends[-2]
        st = ref.standardize(payload["facts"])
        assert st == {k: v for k, v in final.items()}, f"seed {seed}: standardize differs from the generator's truth"
        roic = ref.roic(st, latest, 0.25)
        piot = ref.piotroski_f_score(st, latest)["score"]
        beneish = ref.beneish_m_score(st, latest)["m_score"]
        mj = ref.modified_jones(payload["sample"])
        rows.append(
            (seed, final[latest]["revenue"], roic, piot, beneish, mj["coefficients"][1], mj["discretionary"][0])
        )
        del prev
    print("seed  latest_revenue  roic(25%)  F  M-score  mj_a2  mj_disc[0]")
    for r in rows:
        print(f"{r[0]:>4}  {r[1]:>14.2f}  {r[2]:>9.6f}  {r[3]}  {r[4]:>8.4f}  {r[5]:>9.6f}  {r[6]:>10.6f}")
    print("distinct F-scores:", sorted({r[3] for r in rows}))
    print("distinct M-scores:", len({round(r[4], 9) for r in rows}), "of", len(rows))
    print("distinct roic:", len({round(r[2], 9) for r in rows}), "of", len(rows))
    print("distinct mj a2:", len({round(r[5], 9) for r in rows}), "of", len(rows))
    print("instances whose standardize equals the generator truth: all", len(rows), "of", len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
