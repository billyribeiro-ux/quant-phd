"""Independent check of LX1 project labs: twin run under -I -W error in scratch, page code vs twin, expected vs output."""
import html, re, subprocess, sys, shutil, tempfile, pathlib, os
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c")
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
DATA = ROOT / "course/assets/data/market/fx_monthly.csv"
for n in (1, 2, 3):
    lab_id = f"lab-LX1-project-{n}"
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab_id, PAGE, re.S)
    body = sec.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/LX1/{lab_id}.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{lab_id}: page code == twin (trailing newline aside): {same}")
    if not same:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
    wd = tempfile.mkdtemp(prefix="lx1c-r4-")
    os.makedirs(f"{wd}/data")
    shutil.copy(DATA, f"{wd}/data/fx_monthly.csv")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/LX1/{lab_id}.py")],
                       cwd=wd, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    print(f"  rc={r.returncode} stderr={r.stderr!r}")
    print(f"  stdout == expected block: {r.stdout.rstrip()==exp.rstrip()}")
    open(f"{os.path.dirname(os.path.abspath(__file__))}/out/{lab_id}.stdout","w").write(r.stdout)
    shutil.rmtree(wd)
