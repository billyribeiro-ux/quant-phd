"""Run each LX1 lab twin under python -I -W error and check that every output line appears verbatim
(whitespace-normalised) in its lesson page's visible text. L04 reads data/fx_monthly.csv, so it runs in a
scratch directory that holds a copy of the embedded snapshot under data/.

Run with: python3 -I -W error ledgers/LX1/scripts/LX1-d-r12/lab_text_compare.py <repo-root> <scratch-dir>
"""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
unit = root / "course/modules/LX/LX1"


def page_text(name: str) -> str:
    raw = (unit / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<(?=/?[a-zA-Z!])[^>]*>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


for lesson in ("L01", "L02", "L03", "L04"):
    cwd = scratch / lesson
    (cwd / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy(root / "course/assets/data/market/fx_monthly.csv", cwd / "data/fx_monthly.csv")
    twin = root / f"tests/labs/LX1/lab-LX1-{lesson}-1.py"
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], cwd=cwd, capture_output=True, text=True, check=False
    )
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in run.stdout.splitlines() if ln.strip()]
    text = page_text(lesson)
    missing = [ln for ln in lines if ln not in text]
    print(f"{lesson}: twin exit {run.returncode}, stderr bytes {len(run.stderr)}, output lines {len(lines)}, "
          f"not verbatim in page: {len(missing)}")
    for ln in missing:
        print("   MISSING", ln[:150])
