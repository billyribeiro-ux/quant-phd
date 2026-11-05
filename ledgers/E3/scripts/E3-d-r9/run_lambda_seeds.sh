#!/bin/zsh
cd /tmp/E3d_r9_ws
for s in $(seq 0 49); do
  out=$(QF_SEED=$s /Users/billyribeiro/.fanout/wt/verifyD9-E3-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project_lambda.py -k local_maximum 2>&1 | tail -1)
  echo "seed $s: $out"
done
echo DONE
