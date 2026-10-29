set -u
cd /Users/billyribeiro/.fanout/wt/verifyB9-M2-b
P=.venv/bin/python
echo "== run_labs L07-L12"; for p in L07 L08 L09 L10 L11 L12; do $P tools/run_labs.py --unit M2 --page $p 2>&1 | tail -1; done
echo "== twins isolated"; for p in 07 08 09 10 11 12; do $P -I -W error tests/labs/M2/lab-M2-L$p-1.py >/tmp/m2b9_twin$p.out 2>/tmp/m2b9_twin$p.err; echo "L$p exit=$? stdout_lines=$(wc -l </tmp/m2b9_twin$p.out) stderr_bytes=$(wc -c </tmp/m2b9_twin$p.err)"; done
echo "== page_smoke"; $P tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12 2>&1 | tail -3
echo "== check_pages"; $P tools/check_pages.py --unit M2 2>&1 | tail -3; $P tools/check_pages.py --all 2>&1 | tail -3
echo "== check_dag"; $P tools/check_dag.py --unit M2 2>&1 | tail -3; $P tools/check_dag.py --all 2>&1 | tail -3
echo "== check_projects"; $P tools/check_projects.py --all 2>&1 | tail -3
echo "== ruff"; $P -m ruff check tests tools 2>&1 | tail -2; $P -m ruff format --check tests tools 2>&1 | tail -2
echo "== mypy twins"; $P -m mypy --no-incremental tests/labs/M2/ 2>&1 | tail -2
echo "== pytest labs M2"; $P -m pytest tests/test_labs.py tests/test_run_labs.py -k M2 -q 2>&1 | tail -2
echo "== verify_refs"; $P tools/verify_refs.py --offline 2>&1 | tail -2
echo "== build_site check"; $P tools/build_site.py --check 2>&1 | tail -2
