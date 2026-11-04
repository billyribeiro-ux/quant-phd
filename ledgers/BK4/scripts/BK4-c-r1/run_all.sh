#!/bin/sh
# BK4 slice c, round 1: re-runs every command row and writes its output under out/ (verifier BK4-c r1).
# Usage: sh ledgers/BK4/scripts/BK4-c-r1/run_all.sh   (from anywhere; uses the checkout that contains this file)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
cd "$ROOT" || exit 1
PY="$ROOT/.venv/bin/python"
OUT="$HERE/out"
mkdir -p "$OUT"
: > "$OUT/exit_codes.out"
run() {
  name="$1"; shift
  "$@" > "$OUT/$name.out" 2>&1
  echo "$name EXIT=$?" >> "$OUT/exit_codes.out"
}
run check_projects "$PY" tools/check_projects.py --unit BK4
run check_pages "$PY" tools/check_pages.py --unit BK4
run check_dag "$PY" tools/check_dag.py --unit BK4
run run_labs_project "$PY" tools/run_labs.py --unit BK4 --page project
run run_graders "$PY" tools/run_graders.py --unit BK4 --seeds 0-49
run mutate_graders "$PY" tools/mutate_graders.py --unit BK4 --seeds 0-9
run page_smoke_project "$PY" tools/page_smoke.py --unit BK4 --pages project
run verify_refs_unit "$PY" tools/verify_refs.py --unit BK4
run ruff_check "$PY" -m ruff check tests/labs/BK4 course/modules/BK/BK4/grader
run ruff_format "$PY" -m ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_plan_command "$PY" -m mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_repo_gate "$PY" -m mypy --no-incremental
run mypy_grader_layout "$PY" "$HERE/grader_support.py" typecheck
run pytest_labs "$PY" -m pytest -q -p no:cacheprovider tests/test_labs.py tests/test_run_labs.py
run anchor_check "$PY" "$HERE/anchor_check.py" "$ROOT/course/modules/BK/BK4"
run instance_checks "$PY" "$HERE/instance_checks.py"
run leak_scan "$PY" "$HERE/leak_scan.py"
run float_probe "$PY" "$HERE/float_probe.py"
run probe_large_cents_test "$PY" "$HERE/probe_large_cents_test.py"
run make_mutants "$PY" "$HERE/make_mutants.py"
run make_float_and_unstated "$PY" "$HERE/make_float_and_unstated_mutants.py"
run grade_reference_0_49 "$PY" "$HERE/grade_candidate.py" course/modules/BK/BK4/grader/reference.py 0-49
run grade_starter_0 "$PY" "$HERE/grade_candidate.py" course/modules/BK/BK4/grader/starter.py 0-0
run grade_vc10_0_49 "$PY" "$HERE/grade_candidate.py" ledgers/BK4/mutants/vc10_float_arithmetic.py 0-49
run grade_vc11_0_9 "$PY" "$HERE/grade_candidate.py" "$HERE/unstated_mutants/vc11_sorts_argument_in_place.py" 0-9
for f in "$HERE"/alternatives/*.py; do
  b="$(basename "$f" .py)"
  run "alt_$b" "$PY" "$HERE/grade_candidate.py" "$f" 0-49
done
for f in "$ROOT"/ledgers/BK4/alternatives/*.py; do
  b="$(basename "$f" .py)"
  run "builder_alt_$b" "$PY" "$HERE/grade_candidate.py" "$f" 0-49
done
run collect_only "$PY" "$HERE/grader_support.py" collect
run starter_raw "$PY" "$HERE/grader_support.py" starter
echo done >> "$OUT/exit_codes.out"
