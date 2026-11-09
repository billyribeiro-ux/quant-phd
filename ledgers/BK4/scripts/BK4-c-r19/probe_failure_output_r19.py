"""Round 19 (BK4 slice c): probe what a learner sees when a student module fails, under the suite's own flags.

Each probe writes a modified reference (one change) into a fresh scratch directory with test_project.py and instance.py,
runs `pytest --assert=plain -W error` on seed 0 and prints the report. Usage: python -I probe_failure_output_r19.py <checkout-root>
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
G = ROOT / "course/modules/BK/BK4/grader"
PY = str(ROOT / ".venv/bin/python")
REF = (G / "reference.py").read_text(encoding="utf-8")


def swap(old: str, new: str) -> str:
    assert REF.count(old) == 1, f"search text must occur once: {old!r}"
    return REF.replace(old, new, 1)


PROBES = {
    "A_student_indexerror_in_sizing": (
        swap("    count = len(losses_cents)\n", '    raise IndexError("list index out of range, probe A")\n'),
        "test_fixture_five_losses_at_8000_bps",
    ),
    "B_wrong_sizing_value": (
        swap("    return sorted(losses_cents)[index - 1]", "    return sorted(losses_cents)[index]"),
        "test_fixture_five_losses_at_8000_bps",
    ),
    "C_leftover_cent_dropped": (
        swap("                survivor_cents[member] += 1\n", "                survivor_cents[member] += 0\n"),
        "test_fixture_loss_181",
    ),
    "D_student_typeerror_on_refusal_path": (
        swap("    if loss_cents < 0:", '    raise TypeError("probe D: student code fails")\n    if loss_cents < 0:'),
        "test_negative_loss_is_refused_and_the_message_names_the_loss",
    ),
    "p1_fund_capped_by_defaulter_margin": (
        swap(
            "    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])",
            "    fund_paid = min(loss_cents - margin_paid, initial_margin_cents[defaulter_id])",
        ),
        None,
    ),
    "p3_sizing_strict_above_target": (
        swap(
            "    return sorted(losses_cents)[index - 1]",
            "    return sorted(losses_cents)[min(index, len(losses_cents) - 1) if index * 10_000 == target_bps * count else index - 1]",
        ),
        None,
    ),
    "p4_residual_strictly_above_total": (swap("    if residual >= total_fund:", "    if residual > total_fund:"), None),
    "reference": (REF, None),
}

for name, (src, only) in PROBES.items():
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"bk4r19_{name}_"))
    try:
        shutil.copy(G / "test_project.py", work / "test_project.py")
        shutil.copy(G / "instance.py", work / "instance.py")
        (work / "clearing_house.py").write_text(src, encoding="utf-8")
        cmd = [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"]
        if only:
            cmd[-1:-1] = ["-k", only]
        r = subprocess.run(cmd, cwd=work, env=dict(os.environ, QF_SEED="0"), capture_output=True, text=True)
        print(f"== {name}: exit {r.returncode}")
        print(r.stdout.rstrip("\n"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
