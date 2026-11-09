"""Round-15 lab-mutant writer and harness for SC1 slice a.

Writes the three new student-error lab mutants (SC1a-r15-lab-p1..p3) into ledgers/SC1/lab-mutants/,
then runs every lab mutant under python -I and records whether its output differs from the expected
block of the page it belongs to (killed) or matches it (survived). Usage: python3 -I lab_mutants_r15.py <root>
"""
import os
import re
import subprocess
import sys
import tempfile
import html

root = sys.argv[1]
M = os.path.join(root, "ledgers/SC1/lab-mutants")
tw = {
    "L01": os.path.join(root, "tests/labs/SC1/lab-SC1-L01-1.py"),
    "L02": os.path.join(root, "tests/labs/SC1/lab-SC1-L02-1.py"),
    "L03": os.path.join(root, "tests/labs/SC1/lab-SC1-L03-1.py"),
}
specs = [
    ("SC1a-r15-lab-p1-L01-dyadic-width-doubled.py", "L01", "    width = t / 2**n\n", "    width = t / 2 ** (n + 1)\n",
     "# Mutant: lab-SC1-L01-1: 2**(n+1) pieces, depth sums equal t/2; the 15-of-15 line prints 0 of 15.\n"),
    ("SC1a-r15-lab-p2-L02-level-scale-off-by-half-exponent.py", "L02",
     "        scale = 2 ** (-(m + 1) / 2)\n        for j in range(1, 2 ** (m - 1) + 1):\n            total +=",
     "        scale = 2 ** (-m / 2)\n        for j in range(1, 2 ** (m - 1) + 1):\n            total +=",
     "# Mutant: lab-SC1-L02-1: level scale 2**(-m/2) instead of 2**(-(m+1)/2) in the partial sum.\n"),
    ("SC1a-r15-lab-p3-L03-sd-taken-as-sqrt-horizon-over-steps.py", "L03",
     "    step_sd = math.sqrt(horizon / steps)\n", "    step_sd = math.sqrt(horizon) / steps\n",
     "# Mutant: lab-SC1-L03-1: increment sd sqrt(H)/N instead of sqrt(H/N); the means and z values change.\n"),
]
for name, lid, old, new, header in specs:
    src = open(tw[lid], encoding="utf-8").read()
    assert src.count(old) == 1, name
    open(os.path.join(M, name), "w", encoding="utf-8").write(header + src.replace(old, new, 1))
    print("wrote", name)

expected = {}
for lid, page in [("L01", "L01.html"), ("L02", "L02.html"), ("L03", "L03.html")]:
    t = open(os.path.join(root, "course/modules/SC/SC1", page), encoding="utf-8").read()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S).group(1)
    expected[lid] = html.unescape(e).strip().splitlines()
killed = 0
names = sorted(n for n in os.listdir(M) if n.endswith(".py"))
for name in names:
    src = open(os.path.join(M, name), encoding="utf-8").read()
    m = re.search(r"lab-SC1-(L0\d)", src[:300])
    lid = m.group(1) if m else ("L01" if "L01" in name else "L02" if "L02" in name else "L03")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", os.path.join(M, name)], cwd=d,
                           capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    k = not (out == expected[lid] and r.returncode == 0)
    killed += k
    print(f"{name} [{lid}] rc={r.returncode} {'KILLED (output differs)' if k else 'SURVIVED (identical)'}")
print(f"killed {killed} of {len(names)} lab mutants")
