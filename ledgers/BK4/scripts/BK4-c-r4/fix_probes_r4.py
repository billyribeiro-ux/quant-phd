"""Check that three proposed grader tests (not applied to the course) kill the round-4 survivors, and pass the reference.

Usage: fix_probes_r4.py <checkout_root>. Each proposed test is appended to a scratch copy of test_project.py; the scratch
suite is then run with the reference and with each survivor as clearing_house.py. Nothing under course/ is changed.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
grader = root / "course/modules/BK/BK4/grader"
python = str(root / ".venv/bin/python")
proposed = '''

def test_r4_survivor_order_is_by_id_not_by_dictionary_order() -> None:
    __tracebackhide__ = True
    margins = {3: 1, 1: 1, 2: 1, 4: 0}
    funds = {3: 1, 1: 1, 2: 1, 4: 0}
    result = sol.waterfall(1, 4, margins, funds, 0)
    assert result.survivor_cents == {1: 1, 2: 0, 3: 0}, "the leftover goes to the first survivor by ascending id"


def test_r4_named_refusals_and_uncovered_calls_print_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    __tracebackhide__ = True
    calls = [
        lambda: sol.waterfall(10, 9, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL),
        lambda: sol.waterfall(10, 3, {1: -1, 2: 500, 3: 100}, FIX_FUNDS, FIX_CAPITAL),
        lambda: sol.waterfall(10, 3, FIX_MARGINS, {1: 40, 2: -1, 3: 50}, FIX_CAPITAL),
        lambda: sol.waterfall(10, 3, FIX_MARGINS, FIX_FUNDS, -1),
        lambda: sol.waterfall(300, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL),
        lambda: sol.margin_for_cover([], 9_950),
        lambda: sol.cover_bps([], 10),
        lambda: sol.margin_for_cover([10, -1], 9_950),
    ]
    for call in calls:
        try:
            call()
        except ValueError:
            pass
        captured = capsys.readouterr()
        assert captured.out == "" and captured.err == "", "a named refusal or a valid uncovered call must print nothing"


def test_r4_margin_and_cover_do_not_change_their_list_argument() -> None:
    __tracebackhide__ = True
    losses = [30, 10, 20]
    sol.margin_for_cover(losses, 5_000)
    sol.cover_bps(losses, 20)
    assert losses == [30, 10, 20], "a pure function must not change its list argument"
'''
candidates = {
    "reference": grader / "reference.py",
    "r4a_leftover_in_mapping_order": root / "ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py",
    "r4f_sizing_sorts_caller_list_in_place": root / "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py",
    "r4g_debug_print_on_defaulter_refusal": root / "ledgers/BK4/mutants/r4g_debug_print_on_defaulter_refusal.py",
    "r4h_debug_print_on_uncovered_loss": root / "ledgers/BK4/mutants/r4h_debug_print_on_uncovered_loss.py",
}
for name, cand in candidates.items():
    work = Path(tempfile.mkdtemp(prefix="bk4fix4."))
    try:
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        with (work / "test_project.py").open("a", encoding="utf-8") as fh:
            fh.write(proposed)
        shutil.copy(cand, work / "clearing_house.py")
        env = dict(os.environ, QF_SEED="0", PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run(
            [python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=300,
        )
        print(f"{name}: {(proc.stdout.strip().splitlines() or ['?'])[-1]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
