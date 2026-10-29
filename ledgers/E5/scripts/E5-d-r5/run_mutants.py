"""Run lab-2 student-error mutants and report whether the page's instant check (compare_output, tolerance 1e-6) kills them."""
import glob, html, os, re, subprocess, sys
sys.path.insert(0, os.path.join(sys.argv[1], "tools"))
from coursekit import compare_output
root = sys.argv[1]
page = open(os.path.join(root, "course/modules/E/E5/project.html"), encoding="utf-8").read()
exp = html.unescape(re.findall(r'<pre class="expected" data-tolerance="1e-6">(.*?)</pre>', page, re.S)[1])
files = sorted(glob.glob(os.path.join(root, "ledgers/E5/mutants/project-2*/**/*.py"), recursive=True))
for f in files:
    r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", f], capture_output=True, text=True, cwd="/tmp")
    ok, why = compare_output(r.stdout, exp, 1e-6) if r.returncode == 0 else (False, "exit %d" % r.returncode)
    print("PASSES_CHECK" if ok else "KILLED", os.path.basename(f), why[:120])
