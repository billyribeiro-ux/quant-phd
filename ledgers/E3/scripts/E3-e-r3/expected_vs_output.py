import re, html, subprocess, sys
page = open("course/modules/E/E3/project.html", encoding="utf-8").read()
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?<pre class="expected"[^>]*>(.*?)</pre>' % lab, page, re.S)
    exp = html.unescape(m.group(1)).strip()
    r = subprocess.run([sys.executable, "-I", "-W", "error", "tests/labs/E3/%s.py" % lab.replace("lab-", "lab-")],
                       capture_output=True, text=True)
    out = r.stdout.strip()
    print(lab, "exit", r.returncode, "stderr", repr(r.stderr[:200]), "expected==output:", exp == out)
    if exp != out:
        for a, b in zip(exp.splitlines(), out.splitlines()):
            if a != b:
                print("  expected:", a); print("  output:  ", b)
