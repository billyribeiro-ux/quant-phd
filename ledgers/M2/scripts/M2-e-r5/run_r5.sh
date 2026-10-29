#!/bin/sh
# Commands run by the round-5 verifier for slice M2-e (checkout /tmp/verifyB5-M2-e, pin 09b8751).
# Run from the checkout root. PY is the checkout's venv interpreter.
PY=.venv/bin/python
G=course/modules/M/M2/grader
$PY tools/run_graders.py --unit M2 --seeds 0-49
$PY tools/run_labs.py --unit M2
$PY tools/check_projects.py --unit M2
$PY tools/check_dag.py --unit M2
$PY tools/check_pages.py --unit M2
$PY tools/page_smoke.py --unit M2 --pages project.html --skip-sweep
$PY tools/verify_refs.py --unit M2
$PY tools/verify_refs.py --offline
$PY tools/mutate_graders.py --unit M2 --seeds 0-49
# collect-only count and the reference on sample seeds (workspace = copy of grader + reference as sensitivity_engine.py)
# alternatives: alts/alt_a_richardson_complexstep.py, alts/alt_b_reverse_mode_numpy.py, alts/alt_c_five_point_decimal_cutoffs.py
# each copied to ws/sensitivity_engine.py next to $G/test_project.py and $G/instance.py, then:
#   QF_SEED=<s> $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py   for s in 0..49
# proposed extra test: probe/test_probe_addition.py (copied next to the same files)
# report: report_sim/run_report.py (Lab 3 with the page's replacements) compared with expected block
# browser: reveal_check.py (serves course/ on 127.0.0.1:8765 first)
