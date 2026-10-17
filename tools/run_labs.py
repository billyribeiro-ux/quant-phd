#!/usr/bin/env python3
"""Run every inline lab locally and hold it to its page.

For each ``<section class="lab" data-runtime="python">`` on a unit's pages:

* the lab's code, unescaped, is byte-identical to its twin
  ``tests/labs/<UNIT>/<lab-id>.py`` (trailing newlines aside)
* the twin runs under ``python -I -W error`` with no network, writes nothing to
  stderr, and finishes within the time limit; it runs in a scratch directory
  whose ``data/`` holds exactly the embedded snapshots its section names in
  ``data-files``, so it opens ``data/<file>`` here as it does in the browser
* its stdout matches the page's expected output under the page's own rule
  (numbers within tol·(1+|expected|), other tokens exact; see labs.js)

Completion labs (``class="lab completion"``, project rung 2) show code with
``___`` blanks; for those the twin is the completed solution, every page line
must equal the twin line or contain a blank, and the twin's output must match.

tests/test_labs.py runs the same checks under pytest, so CI covers every lab.

Usage::

    python3 tools/run_labs.py --unit S7
    python3 tools/run_labs.py --all
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time

from coursekit import (
    MARKET_DATA,
    Lab,
    built_units,
    compare_output,
    labs_in,
    load_page,
    market_files,
    snippets_in,
    twin_workdir,
    unit,
)

TIME_LIMIT_S = 30.0
SNIPPET_LIMIT_S = 120.0  # checked solution code is run by the student locally, not on the page


def run_twin(lab: Lab) -> tuple[str, str, float]:
    started = time.perf_counter()
    with twin_workdir(lab.files) as work:
        result = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(lab.twin)],
            capture_output=True,
            text=True,
            timeout=(SNIPPET_LIMIT_S if lab.snippet else TIME_LIMIT_S) * 4,
            check=False,
            env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
            cwd=work,
        )
    elapsed = time.perf_counter() - started
    stderr = result.stderr if result.returncode == 0 else f"exit {result.returncode}\n{result.stderr}"
    return result.stdout, stderr, elapsed


def check_lab(lab: Lab) -> list[str]:
    where = f"{lab.page.name}#{lab.id}"
    if lab.runtime != "python":
        return [f"{where}: runtime {lab.runtime!r} has no local runner yet"]
    if not lab.twin.exists():
        return [f"{where}: missing twin {lab.twin}"]
    twin = lab.twin.read_text(encoding="utf-8").rstrip("\n")
    shown = lab.code.rstrip("\n")
    problems: list[str] = []
    if lab.completion:
        page_lines, twin_lines = shown.split("\n"), twin.split("\n")
        if len(page_lines) != len(twin_lines):
            problems.append(f"{where}: completion code has {len(page_lines)} lines, its twin {len(twin_lines)}")
        else:
            for n, (p, t) in enumerate(zip(page_lines, twin_lines, strict=True), start=1):
                if p != t and "___" not in p:
                    problems.append(f"{where}: line {n} differs from the solution twin without a ___ blank")
        if "___" not in shown:
            problems.append(f"{where}: a completion lab must contain ___ blanks")
    elif shown != twin:
        problems.append(f"{where}: page code is not byte-identical to {lab.twin.name}")
    absent = [f for f in lab.files if f not in market_files() or not (MARKET_DATA / f).is_file()]
    if absent:
        problems.append(f"{where}: data-files {absent} are not embedded snapshots (tools/fetch_data.py)")
    stdout, stderr, elapsed = run_twin(lab)
    if stderr:
        problems.append(f"{where}: stderr/exit not clean: {stderr.strip()[:300]}")
    limit = SNIPPET_LIMIT_S if lab.snippet else TIME_LIMIT_S
    if elapsed > limit:
        problems.append(f"{where}: took {elapsed:.1f} s locally (limit {limit:.0f} s)")
    if lab.expected is None:
        problems.append(f"{where}: no expected output on the page")
    else:
        ok, reason = compare_output(stdout, lab.expected, lab.tolerance)
        if not ok:
            problems.append(f"{where}: output does not match the page ({reason})")
    return problems


def unit_labs(unit_id: str, page: str | None = None) -> list[Lab]:
    found: list[Lab] = []
    for path in unit(unit_id).pages():
        if page is None or path.stem == page:
            page_ = load_page(path)
            found.extend(labs_in(page_) + snippets_in(page_))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true")
    parser.add_argument("--page", help="only the labs on one page of --unit (e.g. L03)")
    args = parser.parse_args()
    targets = [u.id for u in built_units()] if args.all else [args.unit]
    failed = 0
    for unit_id in targets:
        labs = unit_labs(unit_id, args.page)
        bad = 0
        for lab in labs:
            problems = check_lab(lab)
            for problem in problems:
                print(f"FAIL {unit_id}: {problem}")
            bad += bool(problems)
        print(f"run_labs {unit_id}: {'PASS' if not bad else 'FAIL'} ({len(labs) - bad}/{len(labs)})")
        failed += bool(bad)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
