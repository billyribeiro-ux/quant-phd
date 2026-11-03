#!/bin/sh
# Verifier D round 2 evidence: (1) collect-only count of the grader; (2) suite on reference seeds 0-9 with the page flags;
# (3) a Student-t-only sign-flip mutant (not added to mutants/) on seeds 0-9; (4) equivalent m17 on seeds 0-49.
# Usage: sh verifyD2_signt_and_m17.sh <checkout> <scratch>   (scratch holds ref/, signt/, m17eq/ copies)
CO="$1"; S="$2"; PY="$CO/.venv/bin/python"
cd "$S/ref" && QF_SEED=0 "$PY" -m pytest --collect-only -q -p no:cacheprovider 2>&1 | tail -1
for s in 0 1 2 3 4 5 6 7 8 9; do printf "reference seed %s: " $s; (cd "$S/ref" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1); done
for s in 0 1 2 3 4 5 6 7 8 9; do printf "student-t sign flip seed %s: " $s; (cd "$S/signt" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1); done
fails=0; for s in $(seq 0 49); do out=$(cd "$S/m17eq" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1); case "$out" in *failed*) fails=$((fails+1));; esac; done
echo "m17 equivalent: seeds 0-49 with any failure: $fails"
