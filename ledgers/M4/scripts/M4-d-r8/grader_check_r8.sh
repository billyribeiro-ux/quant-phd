#!/bin/bash
# Usage: grader_check_r8.sh <checkout> <scratch>
# Copies grader/*.py into scratch, plus one candidate module as tail_risk.py; runs test_project.py seeds 0..49.
C=$1; S=$2; V=$C/.venv/bin/python
mkdir -p $S/run && cp $C/course/modules/M/M4/grader/*.py $S/run/ && cp "$3" $S/run/tail_risk.py && cd $S/run
out=$(for s in $(seq 0 49); do QF_SEED=$s $V -I -W error -m pytest -p no:cacheprovider -q test_project.py > o_$s.txt 2>&1 && echo ok || echo fail; done | sort | uniq -c)
echo "$3: $out"
