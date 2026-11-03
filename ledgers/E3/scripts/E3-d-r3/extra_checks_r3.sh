#!/bin/sh
# Round-3 verifier (E3-d) extra checks, run from the repository root. Each line prints the observed result.
set -u
PAGE=course/modules/E/E3/project.html
echo "network tokens in project.html (fetch/http/XMLHttpRequest/sendBeacon):"; grep -c -E "fetch\(|https?:|XMLHttp|sendBeacon" $PAGE
echo "banned phrases (BUILDER_RULES 1.3-1.4) in project.html and grader:"; grep -c -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly" $PAGE course/modules/E/E3/grader/*.py
echo "process words in learner text (plan|builder|architect|verifier|fixer|ledger|mutant|orchestrat|placeholder):"; grep -c -i -E "\bplan\b|builder|architect|verifier|fixer|ledger|mutant|orchestrat|placeholder" $PAGE
echo "figures, images, data files on the page:"; grep -c -E "<svg|<img|data-files" $PAGE
echo "kink mentions in project.html and grader/*.py:"; grep -c -i "kink" course/modules/E/E3/project.html course/modules/E/E3/grader/*.py
echo "dominance on the page:"; grep -c -i "dominan" $PAGE
echo "ruff format on the E3 paths:"; .venv/bin/ruff format --check course/modules/E/E3 ledgers/E3 2>&1 | tail -1
echo "registry keys used by the reading list:"; grep -o -E '"(pratt1964risk|kahneman1979prospect|epstein1989substitution|ellsberg1961risk|gilboa1989maxmin)"' references/references.json | sort -u | wc -l
echo "--assert=plain probe (scratch, not in repo):"; mkdir -p /tmp/e3d_r3_assert && cd /tmp/e3d_r3_assert && printf 'def test_x():\n    x = 3\n    assert x == 2\n' > test_assert_probe.py && PYTHONDONTWRITEBYTECODE=1 "$OLDPWD/.venv/bin/python" -B -m pytest -q -p no:cacheprovider --assert=plain test_assert_probe.py 2>&1 | grep -E "^E " ; cd "$OLDPWD"
echo "collect-only count of the grader (scratch copy of the reference as elicit.py):"; sh ledgers/E3/scripts/E3-d-r3/collect_count_r3.sh
