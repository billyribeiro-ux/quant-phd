"""Round-3 LX1-c checks: page code vs twin, twin output vs expected block, run in a scratch dir."""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = sys.argv[1]
PAGE = os.path.join(ROOT, "course/modules/LX/LX1/project.html")
text = open(PAGE, encoding="utf-8").read()
labs = ["lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3"]
for lab in labs:
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, text, re.S)
    body = sec.group(0)
    code = re.search(r"<pre><code[^>]*data-run>(.*?)</code></pre>", body, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin_path = os.path.join(ROOT, "tests/labs/LX1", lab + ".py")
    twin = open(twin_path, encoding="utf-8").read()
    print(lab, "page_code_equals_twin:", code == twin, "len", len(code), len(twin))
    if code != twin:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page"))[:40]))
    tmp = tempfile.mkdtemp(prefix="lx1c-r3-")
    os.makedirs(os.path.join(tmp, "data"))
    shutil.copy(os.path.join(ROOT, "course/assets/data/market/fx_monthly.csv"), os.path.join(tmp, "data"))
    shutil.copy(twin_path, os.path.join(tmp, "lab.py"))
    out = subprocess.run([sys.executable, "-I", "-W", "error", "lab.py"], cwd=tmp, capture_output=True, text=True)
    print(" exit", out.returncode, "stderr:", out.stderr[:300])
    print(" output_equals_expected:", out.stdout.rstrip("\n") == expected.rstrip("\n"))
    if out.stdout.rstrip("\n") != expected.rstrip("\n"):
        print(out.stdout)
    open(os.path.join(os.environ.get("OUTDIR", "/tmp"), lab + ".out"), "w").write(out.stdout)
    shutil.rmtree(tmp)
