#!/bin/bash
# usage: kill_new_mutants.sh <checkout> <python> ; runs each new mutant against the grader on seeds 0-49, stops at first failing seed
C=$1; P=$2; G=$C/course/modules/M/M3/grader
for n in r14d_m01_clip_rebuild_uses_transposed_vectors r14d_m02_comparison_weights_unnormalised r14d_m03_projection_one_iteration; do
  d=$(mktemp -d /tmp/m3d14mut.XXXX); cp $G/test_project.py $G/instance.py $d/; cp $C/ledgers/M3/mutants/$n.py $d/covariance_doctor.py
  r=SURVIVED
  for s in $(seq 0 49); do
    if ! (cd $d && QF_SEED=$s $P -I -W error -m pytest -q -p no:cacheprovider --assert=plain test_project.py >/dev/null 2>&1); then r="KILLED seed $s"; break; fi
  done
  echo "$n $r"
done
