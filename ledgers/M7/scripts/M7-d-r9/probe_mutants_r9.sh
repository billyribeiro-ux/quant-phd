#!/bin/bash
# Round 9: run named mutants through the suite on seeds 0-9; print the first failing test (or SURVIVED).
CK=/Users/billyribeiro/.fanout/wt/verifyD9-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r9
for name in "$@"; do
  f=$(ls $CK/ledgers/M7/mutants/${name}*.py | head -1)
  killed="SURVIVED seeds 0-9"
  for seed in $(seq 0 9); do
    out=$($S/grader_suite_r9.sh "$f" $seed /tmp/m7d-r9/probe_$seed-$name -rf 2>&1)
    if ! echo "$out" | grep -qE "^364 passed in"; then
      killed="KILLED seed $seed: $(echo "$out" | grep '^FAILED' | head -1 | cut -c1-220)"
      break
    fi
  done
  echo "$(basename $f) :: $killed"
done
