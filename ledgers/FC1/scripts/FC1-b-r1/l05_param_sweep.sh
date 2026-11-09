#!/bin/sh
# Runs the L05 twin with one parameter changed in a scratch copy (never the repo file).
# usage: l05_param_sweep.sh <repo-root> <scratch-dir>
ROOT="$1"; SCR="$2"; mkdir -p "$SCR"
TWIN="$ROOT/tests/labs/FC1/lab-FC1-L05-1.py"
run() { name="$1"; sed "$2" "$TWIN" > "$SCR/$name.py"; "$ROOT/.venv/bin/python" -I -W error "$SCR/$name.py" > "$SCR/$name.out" 2>&1; echo "$name rc=$?"; }
run base 's/XXXX_NOPE//'
run settle3 's/^SETTLEMENT_LAG = 2 /SETTLEMENT_LAG = 3 /'
run clear1 's/^CLEARING_OFFSET = 0 /CLEARING_OFFSET = 1 /'
run clear3 's/^CLEARING_OFFSET = 0 /CLEARING_OFFSET = 3 /'
run clear2_lag2 's/^CLEARING_OFFSET = 0 /CLEARING_OFFSET = 2 /'
