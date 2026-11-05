"""Re-run the six existing lab-claim mutants in ledgers/SC1/lab-mutants against the page expected blocks.

Each mutant runs with python -I -W error from an empty directory; killed when it fails or its stdout differs
from the expected block of the page that owns its twin.
"""
import html, re, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1])
for mut in sorted((root / "ledgers/SC1/lab-mutants").glob("*.py")):
    page = "L01" if "L01" in mut.name else "L02" if "L02" in mut.name else "L03"
    h = (root / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', h, re.S).group(1)).rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(mut)], cwd=scratch, capture_output=True, text=True)
    out = p.stdout.rstrip("\n")
    killed = p.returncode != 0 or out != expected
    diff = next((f"expected={a!r} got={b!r}" for a, b in zip(expected.splitlines(), out.splitlines()) if a != b), "no line differs")
    print(f"{mut.name}: exit={p.returncode} killed={killed} first_diff={diff}")
