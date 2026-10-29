"""Round 4, slice M5-b: run the L05-L07 twins under python -I -W error and compare with the page's embedded output."""
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = root / ".venv" / "bin" / "python"
for lesson in ("L05", "L06", "L07"):
    twin = root / "tests" / "labs" / "M5" / f"lab-M5-{lesson}-1.py"
    run = subprocess.run([str(py), "-I", "-W", "error", str(twin)], capture_output=True, text=True, timeout=60)
    html = (root / "course" / "modules" / "M" / "M5" / f"{lesson}.html").read_text()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html, re.S)
    expected = m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    print(lesson, "exit", run.returncode, "embedded==run", expected.strip() == run.stdout.strip())
