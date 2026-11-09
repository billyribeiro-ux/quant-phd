"""Round-14 verifier: runs each alternative (alts/alt*.py) alone under python -I -W error in a scratch directory with
data/fx_monthly.csv, and compares its stdout with the page's expected block. Argument 1 is the checkout root."""
import importlib.util, pathlib, sys, glob, os, re, shutil, subprocess, tempfile, html
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
def expected(lab):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).rstrip("\n")
for path in sorted(glob.glob(str(pathlib.Path(__file__).parent / "alts/alt*.py"))):
    text = open(path, encoding="utf-8").read()
    lab = "lab-LX1-project-" + ("3" if "lab3" in os.path.basename(path) else "1" if "lab1" in os.path.basename(path) else "2")
    wd = tempfile.mkdtemp(prefix="r14alt-")
    try:
        os.makedirs(f"{wd}/data")
        shutil.copy(root / "course/assets/data/market/fx_monthly.csv", f"{wd}/data/fx_monthly.csv")
        shutil.copy(path, f"{wd}/lab.py")
        p = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", f"{wd}/lab.py"], cwd=wd,
                           capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"}, timeout=120)
    finally:
        shutil.rmtree(wd)
    ok = p.returncode == 0 and not p.stderr and p.stdout.rstrip("\n") == expected(lab)
    print("MATCH" if ok else "NO-MATCH", "|", os.path.basename(path), "|", lab, "| rc", p.returncode,
          "| stderr", p.stderr.strip()[-200:])
    if not ok and p.returncode == 0:
        import difflib
        print("\n".join(list(difflib.unified_diff(expected(lab).splitlines(), p.stdout.rstrip("\n").splitlines(), lineterm=""))[:20]))
