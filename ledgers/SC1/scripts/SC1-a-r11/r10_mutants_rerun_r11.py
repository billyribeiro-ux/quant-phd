"""Re-run of the four round-10 lab mutants (ledgers/SC1/mutants/SC1-a-r10/) against the page expected blocks."""

import html
import re
import subprocess
import sys
import tempfile

REPO = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a"
MUTS = [
    "ledgers/SC1/mutants/SC1-a-r10/mut-L01-1.py",
    "ledgers/SC1/mutants/SC1-a-r10/mut-L02-1.py",
    "ledgers/SC1/mutants/SC1-a-r10/mut-L03-1.py",
    "ledgers/SC1/mutants/SC1-a-r10/mut-L03-2.py",
]
PAGES = {
    "L01": f"{REPO}/course/modules/SC/SC1/L01.html",
    "L02": f"{REPO}/course/modules/SC/SC1/L02.html",
    "L03": f"{REPO}/course/modules/SC/SC1/L03.html",
}


def expected(lab: str) -> str:
    text = open(PAGES[lab], encoding="utf-8").read()
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).strip()


for rel in MUTS:
    path = f"{REPO}/{rel}"
    lab = re.search(r"mut-(L0\d)", rel).group(1)
    with tempfile.TemporaryDirectory(prefix="r10m") as d:
        p = subprocess.run([sys.executable, "-I", "-W", "error", path], cwd=d, capture_output=True, text=True, timeout=120)
    same = p.stdout.strip() == expected(lab)
    print(f"{rel.split('/')[-1]} rc={p.returncode} stderr_bytes={len(p.stderr)} matches_expected={same} -> {'SURVIVED' if same else 'KILLED'}")
