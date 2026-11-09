"""LX1-c round 19: runs the three project labs (python -I -W error) and recomputes the prose numbers.

Usage: python -I project_claims_r19.py <checkout_root>. Lab 3 runs in a scratch dir holding data/fx_monthly.csv.
Compares each run's stdout with the page's expected block (html-unescaped), then prints the unrounded values behind
each number the project prose quotes.
"""
import html
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1]).resolve()
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")


def section(lab_id: str) -> str:
    start = page.index(f'id="{lab_id}"')
    return page[start:page.index("</section>", start)]


def expected(lab_id: str) -> str:
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section(lab_id), re.S)
    return html.unescape(m.group(1)).rstrip("\n")


def run(lab_id: str, snapshot: bool) -> tuple[int, str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        if snapshot:
            (pathlib.Path(tmp) / "data").mkdir()
            shutil.copy(root / "course/assets/data/market/fx_monthly.csv", pathlib.Path(tmp) / "data" / "fx_monthly.csv")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/LX1/{lab_id}.py")],
                           cwd=tmp, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


for lab_id, snap in (("lab-LX1-project-1", False), ("lab-LX1-project-2", False), ("lab-LX1-project-3", True)):
    rc, out, err = run(lab_id, snap)
    print(f"{lab_id}: rc={rc} stderr_bytes={len(err)} stdout==page expected: {out.rstrip(chr(10)) == expected(lab_id)}")

values = {
    "Lab 1 real value period 5, falling path (dollars)": 10000000 / 0.85 / 100,
    "Lab 1 burden change, falling path (percent)": 100 * (1 / 0.85 - 1),
    "Lab 1 burden change, rising path (percent)": 100 * (1 / 1.15 - 1),
    "Lab 1 difference of period-5 real values (dollars)": (10000000 / 0.85 - 10000000 / 1.15) / 100,
    "Lab 2 real value period 5 (dollars)": 4000000 / 0.93 / 100,
    "Lab 2 burden change (percent)": 100 * (1 / 0.93 - 1),
    "Lab 2 burden change with the ratio inverted (percent)": 100 * (0.93 / 1 - 1),
}
for name, value in values.items():
    print(f"{name}: unrounded {value:.6f}")
