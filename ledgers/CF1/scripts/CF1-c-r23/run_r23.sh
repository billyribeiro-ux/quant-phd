#!/bin/sh
# Round 23 (slice c) re-run of the command rows; outputs in out/. Usage: run_r23.sh <checkout> <scratch>
CK=$1; S=$2; P=$CK/.venv/bin/python; O=$CK/ledgers/CF1/scripts/CF1-c-r23/out
cd "$CK" || exit 1
git rev-parse HEAD > "$O/pin.txt"
$P tools/check_pages.py --all > "$O/check_pages.txt" 2>&1; echo "check_pages rc=$?" >> "$O/check_pages.txt"
$P tools/check_dag.py --all > "$O/check_dag.txt" 2>&1; echo "check_dag rc=$?" >> "$O/check_dag.txt"
$P tools/run_labs.py --unit CF1 > "$O/run_labs.txt" 2>&1; echo "run_labs rc=$?" >> "$O/run_labs.txt"
$P tools/page_smoke.py --unit CF1 --pages L05 L06 > "$O/page_smoke.txt" 2>&1; echo "page_smoke rc=$?" >> "$O/page_smoke.txt"
$P -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py > "$O/pytest_labs.txt" 2>&1; echo "pytest rc=$?" >> "$O/pytest_labs.txt"
$P tools/verify_refs.py --offline > "$O/verify_refs_offline.txt" 2>&1; echo "rc=$?" >> "$O/verify_refs_offline.txt"
$P tools/verify_refs.py --unit CF1 > "$O/verify_refs_unit.txt" 2>&1; echo "rc=$?" >> "$O/verify_refs_unit.txt"
$P -m ruff check tests/labs/CF1 > "$O/ruff.txt" 2>&1; $P -m ruff format --check tests/labs/CF1 >> "$O/ruff.txt" 2>&1
$P -m mypy --no-incremental tests/labs/CF1/lab-CF1-L05-1.py tests/labs/CF1/lab-CF1-L06-1.py > "$O/mypy.txt" 2>&1; echo "mypy rc=$?" >> "$O/mypy.txt"
$P -I -W error tests/labs/CF1/lab-CF1-L05-1.py > "$O/lab_L05.out" 2>"$O/lab_L05.err"; echo "rc=$?" > "$O/lab_L05.rc"
$P -I -W error tests/labs/CF1/lab-CF1-L06-1.py > "$O/lab_L06.out" 2>"$O/lab_L06.err"; echo "rc=$?" > "$O/lab_L06.rc"
$P -I "$CK/ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py" "$CK" > "$O/twin_vs_page.txt" 2>&1
sh "$CK/ledgers/CF1/scripts/CF1-c-r20/collect_project_r20.sh" "$CK" "$S/collect" > "$O/collect_157.txt" 2>&1
sh "$CK/ledgers/CF1/scripts/CF1-c-r20/run_lab_mutants_r20.sh" "$CK" "$S/mut" > "$O/lab_mutants.txt" 2>&1
$P -I "$CK/ledgers/CF1/scripts/CF1-c-r23/recompute_L06.py" > "$O/recompute_L06.txt" 2>&1
$P -I "$CK/ledgers/CF1/scripts/CF1-c-r23/lab06_unrounded.py" "$CK/tests/labs/CF1/lab-CF1-L06-1.py" > "$O/lab06_unrounded.txt" 2>&1
$P -I "$CK/ledgers/CF1/scripts/CF1-c-r16/banned_scan_r16.py" "$CK/course/modules/CF/CF1/L05.html" "$CK/course/modules/CF/CF1/L06.html" > "$O/banned_scan.txt" 2>&1
echo done
