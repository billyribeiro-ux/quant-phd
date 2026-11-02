#!/bin/bash
# Round-1 misc checks for M7 slice d. Usage: misc_checks_r1.sh <checkout-root>
set -u
R="$1"; PY="$R/.venv/bin/python"; G="$R/course/modules/M/M7/grader"
echo "== collected tests per seed 0-49 (local pytest, reference as solution)"
W=$(mktemp -d /tmp/m7d-collect.XXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/reference.py" "$W/constrained_allocator.py"
(cd "$W" && for s in $(seq 0 49); do QF_SEED=$s PYTHONHASHSEED=0 "$PY" -m pytest --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done | sort | uniq -c)
echo "== decode command on the project page (python3, run from the grader folder)"
(cd "$G" && python3 -c "import json; from instance import make_instance; print(sorted(json.loads(make_instance(7)['payload'])))")
echo "== banned phrases and external links in project.html"
grep -n -i -E "todo|tbd|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important|studies show|experts agree|well known|obviously|clearly|https?://" "$R/course/modules/M/M7/project.html" || echo "none"
echo "== reference.py deployment exclusion evidence"
grep -n -i "reference" "$R/.gitignore" "$R/.github/workflows/ci.yml" 2>/dev/null || echo "no exclusion for reference.py in .gitignore or CI"
ls "$R/.vercelignore" "$R/vercel.json" 2>/dev/null || echo "no .vercelignore or vercel.json in the repository"
