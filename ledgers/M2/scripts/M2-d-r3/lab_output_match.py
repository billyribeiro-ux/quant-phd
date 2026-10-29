"""Run each slice lab twin in isolated mode and check every printed line appears in its lesson page.

Usage: <checkout>/.venv/bin/python -I lab_output_match.py <checkout>
"""
import html
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
python = checkout / ".venv" / "bin" / "python"
for n in range(19, 25):
    twin = checkout / "tests" / "labs" / "M2" / f"lab-M2-L{n}-1.py"
    run = subprocess.run([str(python), "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=True)
    page = html.unescape((checkout / "course" / "modules" / "M" / "M2" / f"L{n}.html").read_text(encoding="utf-8"))
    lines = [line for line in run.stdout.splitlines() if line.strip()]
    missing = [line for line in lines if line not in page]
    print(f"L{n}: {len(lines)} printed lines, {len(missing)} missing from page")
