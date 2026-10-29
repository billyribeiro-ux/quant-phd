"""Round-5 runs: project lab twins against embedded expected output; alternatives and the proposed probe test
against the current grader over seeds 0-49. Run from the checkout root with its venv interpreter."""
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(".").resolve()
PY = str(ROOT / ".venv/bin/python")
SCR = ROOT / "ledgers/M2/scripts/M2-e-r5"
G = ROOT / "course/modules/M/M2/grader"
page = (ROOT / "course/modules/M/M2/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for n in (1, 2, 3):
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M2/lab-M2-project-{n}.py")],
                         capture_output=True, text=True)
    exp = html.unescape(blocks[n - 1]).strip()
    print(f"twin project-{n}: exit {out.returncode}; stdout equals embedded expected block: {out.stdout.strip() == exp}")

impls = {
    "reference": G / "reference.py",
    "alt_a_richardson_complexstep": SCR / "alts/alt_a_richardson_complexstep.py",
    "alt_b_reverse_mode_numpy": SCR / "alts/alt_b_reverse_mode_numpy.py",
    "alt_c_five_point_decimal_cutoffs": SCR / "alts/alt_c_five_point_decimal_cutoffs.py",
    "v01_mutant": ROOT / "ledgers/M2/mutants/v01_ad_derivative_is_a_central_difference_not_dual.py",
}
probe = SCR / "probe/test_probe_addition.py"
for name, src in impls.items():
    ws = Path("/tmp/M2-v/M2-e-r5/ws-r5-" + name)
    shutil.rmtree(ws, ignore_errors=True)
    ws.mkdir(parents=True)
    shutil.copy(G / "test_project.py", ws)
    shutil.copy(G / "instance.py", ws)
    shutil.copy(src, ws / "sensitivity_engine.py")
    shutil.copy(probe, ws / "test_probe_addition.py")
    failed = []
    for seed in range(50):
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=ws, env={"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"},
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(seed)
    rp = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                         "test_probe_addition.py"], cwd=ws, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"},
                        capture_output=True, text=True)
    print(f"{name}: suite failing seeds (0-49): {failed if failed else 'none'}; "
          f"proposed AD exactness test: {'passes' if rp.returncode == 0 else 'fails'}")
