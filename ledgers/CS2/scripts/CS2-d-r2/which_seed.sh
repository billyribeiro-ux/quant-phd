#!/bin/sh
# For each seed 0-49, run the suite against the mutant m11 and print seeds that fail.
W=$(mktemp -d /tmp/CS2-v/d2/ws-m11.XXXX)
cp /tmp/verifyB2-CS2-d/course/modules/CS/CS2/grader/test_project.py /tmp/verifyB2-CS2-d/course/modules/CS/CS2/grader/instance.py "$W"/
cp /tmp/verifyB2-CS2-d/ledgers/CS2/mutants/m11_rank_target_float_cutoff.py "$W"/streamstats.py
cd "$W"
for s in $(seq 0 49); do
  if ! QF_SEED=$s /tmp/verifyB2-CS2-d/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1; then echo "seed $s fails"; fi
done
echo done
