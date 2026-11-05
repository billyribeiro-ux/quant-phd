#!/bin/bash
# M2-d2 r10: the extra commands run this round (outputs recorded in out/). Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
S=ledgers/M2/scripts/M2-d2-r10; O=$S/out; P=.venv/bin/python
for L in L22 L24; do d=$(mktemp -d /tmp/m2d2r10_XXXX); (cd "$d" && "$OLDPWD/$P" -I -W error "$OLDPWD/tests/labs/M2/lab-M2-$L-1.py" > out.txt 2> err.txt; echo "$L exit=$? stderr_bytes=$(wc -c < err.txt)"); done
d=$(mktemp -d /tmp/m2d2r10_XXXX); (cd "$d" && "$OLDPWD/$P" -I -W error "$OLDPWD/tests/labs/M2/lab-M2-L23-1.py" > out.txt 2> err.txt; echo "L23 exit=$? stderr_bytes=$(wc -c < err.txt)")
$P tools/verify_refs.py --unit M2 > $O/verify_refs_live_M2.txt 2>&1; echo "exit=$?" >> $O/verify_refs_live_M2.txt
$P -m ruff check . > $O/ruff_check_repo.txt 2>&1; $P -m ruff format --check . > $O/ruff_format_repo.txt 2>&1
$P -m mypy --no-incremental > $O/mypy_repo.txt 2>&1
$P tools/render_curriculum.py > $O/render_curriculum.txt 2>&1; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $O/render_diff.txt 2>&1; echo "diff-exit=$?" >> $O/render_diff.txt
$P tools/check_projects.py --all > $O/check_projects_all.txt 2>&1
$P tools/run_graders.py --unit M2 --seeds 0-49 > $O/run_graders_M2.txt 2>&1
$P tools/mutate_graders.py --unit M2 --seeds 0-9 > $O/mutate_graders_M2.txt 2>&1
