#!/bin/bash
# Round 16: run the three project lab twins alone under python -I -W error, stderr captured, outputs kept in out/.
R=/Users/billyribeiro/.fanout/wt/verifyE16-E4-d
PY=/Users/billyribeiro/.local/share/mise/installs/python/3.14.8/bin/python3.14
O=$R/ledgers/E4/scripts/E4-d-r16/out
cd "$R" || exit 1
for n in 1 2 3; do
  "$PY" -I -W error tests/labs/E4/lab-E4-project-$n.py > $O/twin_project_$n.out 2> $O/twin_project_$n.err
  echo "twin project-$n exit $? stderr_bytes $(wc -c < $O/twin_project_$n.err)"
done
