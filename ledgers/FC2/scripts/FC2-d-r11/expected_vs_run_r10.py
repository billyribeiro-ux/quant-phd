"""For each project.html lab (1..3): compare the page's expected block with the stdout of the lab's twin (run under python -I -W error from /tmp)."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/FC/FC2/project.html", encoding="utf-8").read()
sections = re.findall(r'<section class="lab[^"]*" id="lab-FC2-project-(\d)".*?</section>', page, re.S)
for n in ("1", "2", "3"):
    m = re.search(rf'<section class="lab[^"]*" id="lab-FC2-project-{n}".*?</section>', page, re.S)
    body = m.group(0)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
    exp = html.unescape(exp).rstrip("\n")
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/FC2/lab-FC2-project-{n}.py"],
                         capture_output=True, text=True, cwd="/tmp")
    got = out.stdout.rstrip("\n")
    print(f"lab {n}: rc={out.returncode} stderr_bytes={len(out.stderr)} expected_equals_output={exp == got} expected_lines={len(exp.splitlines())} output_lines={len(got.splitlines())}")
