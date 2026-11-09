#!/bin/sh
# LX2-c closing delta, round 1: the commands run at pin 95f3f8cb, in this order. Outputs are in out/r1_*.
# Run from the checkout root. Each command was run alone; the exit code is recorded in its output file.
set -u
D=ledgers/LX2/scripts/LX2-c-r1
.venv/bin/ruff check . > $D/out/r1_ruff_check.txt 2>&1
.venv/bin/ruff format --check . > $D/out/r1_ruff_format.txt 2>&1
.venv/bin/mypy --no-incremental > $D/out/r1_mypy.txt 2>&1
.venv/bin/python tools/check_pages.py --unit LX2 > $D/out/r1_check_pages_LX2.txt 2>&1
.venv/bin/python tools/check_dag.py --all > $D/out/r1_check_dag.txt 2>&1
.venv/bin/python tools/check_projects.py --unit LX2 > $D/out/r1_check_projects_LX2.txt 2>&1
.venv/bin/python tools/run_labs.py --unit LX2 > $D/out/r1_run_labs_LX2.txt 2>&1
.venv/bin/python tools/run_graders.py --unit LX2 > $D/out/r1_run_graders_LX2.txt 2>&1
.venv/bin/python tools/mutate_graders.py --unit LX2 > $D/out/r1_mutate_graders_LX2.txt 2>&1
.venv/bin/python tools/page_smoke.py --unit LX2 --pages project > $D/out/r1_page_smoke_project.txt 2>&1
.venv/bin/python tools/verify_refs.py --offline > $D/out/r1_verify_refs_offline.txt 2>&1
.venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py -k 'LX2 or project' > $D/out/r1_pytest_subset.txt 2>&1
for n in 1 2 3; do
  python3 -I -W error tests/labs/LX2/lab-LX2-project-$n.py > $D/out/r1_twin_project_$n.stdout 2> $D/out/r1_twin_project_$n.stderr
done
.venv/bin/python $D/page_vs_twin_r1.py > $D/out/r1_page_vs_twin.txt 2>&1
.venv/bin/python $D/lab2_harness_r1.py > $D/out/r1_lab2_harness.txt 2>&1
.venv/bin/python -I $D/../LX2-c-r12/rederive_r12.py > $D/out/r1_rederive_r12_rerun.txt 2>&1
.venv/bin/python tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $D/out/r1_render_curriculum.txt 2>&1
.venv/bin/python tools/build_site.py --check > $D/out/r1_build_site_check.txt 2>&1
# Byte identity of the slice inputs between the base pin and HEAD (empty output means identical):
git diff --name-only 5db69a9b HEAD -- course/modules/LX/LX2/project.html tests/labs/LX2/lab-LX2-project-1.py tests/labs/LX2/lab-LX2-project-2.py tests/labs/LX2/lab-LX2-project-3.py course/assets/js/labs.js course/assets/js/rubric.js course/modules/LX/LX2/index.html course/modules/LX/LX2/L04.html notation/notation.json curriculum/06-profession-capstone.yaml plans/LX2-build-plan.md > $D/out/r1_identity.txt
