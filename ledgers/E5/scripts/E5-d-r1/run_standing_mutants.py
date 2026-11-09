"""Run every standing lab-2 student-error mutant and alternative (ledgers/E5/mutants/project-2*) against the
project page's expected block for lab 2 (compare_output, tolerance 1e-6), exactly as the page's instant check does."""
import glob, html, os, re, subprocess, sys
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "tools"))
from coursekit import compare_output
page = open(os.path.join(root, "course/modules/E/E5/project.html"), encoding="utf-8").read()
exp = html.unescape(re.findall(r'<pre class="expected" data-tolerance="1e-6">(.*?)</pre>', page, re.S)[1])
files = sorted(glob.glob(os.path.join(root, "ledgers/E5/mutants/project-2*/**/*.py"), recursive=True))
for f in files:
    r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", f], capture_output=True, text=True, cwd="/tmp")
    ok, why = compare_output(r.stdout, exp, 1e-6) if r.returncode == 0 else (False, "exit %d" % r.returncode)
    print("PASSES_CHECK" if ok else "KILLED", os.path.relpath(f, root), why[:110])
print("total", len(files))
