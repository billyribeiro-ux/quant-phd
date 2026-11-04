#!/bin/bash
# usage: v6_run_suite.sh <candidate.py> <seed> [pytest args...]
# Copies instance.py, test_project.py and the candidate (as streamstats.py) into a fresh scratch dir and runs the suite.
CHECKOUT="$(cd "$(dirname "$0")/../../../.." && pwd)"
CAND="$1"; SEED="$2"; shift 2
DIR="$(mktemp -d /tmp/v6cs2d.XXXXXX)"
cp "$CHECKOUT/course/modules/CS/CS2/grader/instance.py" "$CHECKOUT/course/modules/CS/CS2/grader/test_project.py" "$DIR/"
cp "$CAND" "$DIR/streamstats.py"
cd "$DIR" && QF_SEED="$SEED" "$CHECKOUT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error "$@" test_project.py
