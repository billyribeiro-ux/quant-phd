"""Round-9 verifier: for each project lab on project.html, (a) the page code equals the twin (completion lab 2:
page lines equal twin lines except blanked lines), (b) the twin runs alone under python -I -W error in a scratch
dir with data/ (lab 3 only), (c) the stdout equals the page expected block token-for-token. Argument 1 is the
checkout root. Prints one line per lab. Exit 0 only if all pass."""
import html, pathlib, re, subprocess, sys, tempfile, shutil, os
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
ok_all = True
for lab in ["lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3"]:
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    completion = 'class="lab completion"' in sec
    code_html = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
    code = html.unescape(code_html)
    twin = (root / f"tests/labs/LX1/{lab}.py").read_text(encoding="utf-8")
    if not completion:
        same = code.rstrip("\n") == twin.rstrip("\n")
        print(lab, "page code == twin:", same, "(page len", len(code), "twin len", len(twin), ")")
        ok_all &= same
    else:
        pl, tl = code.rstrip("\n").split("\n"), twin.rstrip("\n").split("\n")
        mism = []
        if len(pl) != len(tl):
            mism.append(("len", len(pl), len(tl)))
        for i, (a, b) in enumerate(zip(pl, tl), 1):
            if a != b and "___" not in a:
                mism.append((i, a, b))
        blanks = [i for i, a in enumerate(pl, 1) if "___" in a]
        print(lab, "completion: page lines", len(pl), "twin lines", len(tl), "blank lines", blanks, "mismatches", mism)
        ok_all &= (not mism)
    exp_html = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    expected = html.unescape(exp_html)
    wd = tempfile.mkdtemp(prefix="v9lab-")
    try:
        os.makedirs(f"{wd}/data")
        if "data-files" in sec:
            shutil.copy(root / "course/assets/data/market/fx_monthly.csv", f"{wd}/data/fx_monthly.csv")
        shutil.copy(root / f"tests/labs/LX1/{lab}.py", f"{wd}/lab.py")
        p = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", f"{wd}/lab.py"], cwd=wd,
                           capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"}, timeout=60)
    finally:
        shutil.rmtree(wd)
    exact = p.stdout.rstrip("\n") == expected.rstrip("\n")
    print(lab, "rc", p.returncode, "stderr", repr(p.stderr[:200]), "stdout==expected exact:", exact,
          "lines", len(p.stdout.splitlines()))
    if not exact:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), p.stdout.splitlines(), lineterm="")))
    ok_all &= (p.returncode == 0 and not p.stderr and exact) or (completion and p.returncode == 0)
print("ALL", ok_all)
