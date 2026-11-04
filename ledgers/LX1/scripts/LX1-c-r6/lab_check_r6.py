"""Round-6 lab check for LX1-c: page code == twin, twin runs under python -I -W error, stdout == expected block."""
import html, os, re, shutil, subprocess, sys, tempfile, pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE6-LX1-c")
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
DATA = ROOT / "course/assets/data/market/fx_monthly.csv"

for n in (1, 2, 3):
    sec = re.search(r'<section class="lab[^"]*" id="lab-LX1-project-%d".*?</section>' % n, PAGE, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp_m = re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', sec, re.S)
    exp = html.unescape(exp_m.group(2))
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-project-{n}.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    wd = tempfile.mkdtemp(prefix="lx1c-r6-lab-")
    os.makedirs(f"{wd}/data")
    shutil.copy(DATA, f"{wd}/data/fx_monthly.csv")
    tw = pathlib.Path(wd) / "twin.py"
    tw.write_text(twin, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(tw)], cwd=wd, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    shutil.rmtree(wd)
    print(f"lab {n}: page_code==twin {same}; rc={r.returncode}; stderr_empty={r.stderr.strip()==''}; stdout==expected {r.stdout.rstrip()==exp.rstrip()}; tol={exp_m.group(1)}")
    if r.stdout.rstrip() != exp.rstrip():
        print("DIFF"); print(r.stdout); print(exp)
