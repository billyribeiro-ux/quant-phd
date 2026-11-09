#!/bin/bash
# Round 6 gate run for FC2 slice a at pin e896b7a4 (run from checkout root).
set -u
P=.venv/bin/python
D=ledgers/FC2/scripts/FC2-a-r6
echo "== check_pages FC2"; $P tools/check_pages.py --unit FC2; echo "rc=$?"
echo "== check_dag FC2"; $P tools/check_dag.py --unit FC2; echo "rc=$?"
echo "== check_projects FC2"; $P tools/check_projects.py --unit FC2; echo "rc=$?"
echo "== run_labs FC2"; $P tools/run_labs.py --unit FC2; echo "rc=$?"
for p in L01 L02 L03; do echo "== run_labs page $p"; $P tools/run_labs.py --unit FC2 --page $p; echo "rc=$?"; done
for l in L01 L02 L03; do echo "== twin alone $l"; $P -I -W error tests/labs/FC2/lab-FC2-$l-1.py > $D/r6-twin-$l.out 2> $D/r6-twin-$l.err; echo "rc=$? stderr_bytes=$(wc -c < $D/r6-twin-$l.err)"; done
echo "== page_smoke"; $P tools/page_smoke.py --unit FC2 --pages index.html L01.html L02.html L03.html; echo "rc=$?"
echo "== ruff check twins"; .venv/bin/ruff check tests/labs/FC2/lab-FC2-L01-1.py tests/labs/FC2/lab-FC2-L02-1.py tests/labs/FC2/lab-FC2-L03-1.py; echo "rc=$?"
echo "== ruff format twins"; .venv/bin/ruff format --check tests/labs/FC2/lab-FC2-L01-1.py tests/labs/FC2/lab-FC2-L02-1.py tests/labs/FC2/lab-FC2-L03-1.py; echo "rc=$?"
echo "== mypy twins"; .venv/bin/mypy --no-incremental tests/labs/FC2/lab-FC2-L01-1.py tests/labs/FC2/lab-FC2-L02-1.py tests/labs/FC2/lab-FC2-L03-1.py; echo "rc=$?"
echo "== pytest"; $P -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py tests/test_docs_figures.py 2>&1 | tail -15; echo "rc=${PIPESTATUS[0]}"
echo "== verify_refs offline"; $P tools/verify_refs.py --offline; echo "rc=$?"
echo "== build_site --check"; $P tools/build_site.py --check; echo "rc=$?"
