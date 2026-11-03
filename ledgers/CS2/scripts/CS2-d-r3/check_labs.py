import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-CS2-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("labs found:", [b[0] for b in blocks])
for lab_id, code_html, exp_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(exp_html)
    twin = (root / "tests/labs/CS2" / f"lab-CS2-{lab_id[4:]}.py".replace("lab-CS2-", "lab-CS2-")).read_text(encoding="utf-8") if False else None
    tw = root / "tests/labs/CS2" / (lab_id + ".py")
    twin_src = tw.read_text(encoding="utf-8")
    print(lab_id, "page code == twin:", code == twin_src, "| page code len", len(code), "twin len", len(twin_src))
    if code != twin_src:
        import difflib
        print("".join(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "page")))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(tw)], capture_output=True, text=True, timeout=120)
    print(lab_id, "twin exit", r.returncode, "stderr", repr(r.stderr[:200]))
    out = r.stdout
    print(lab_id, "output == expected block:", out.strip() == expected.strip())
    if out.strip() != expected.strip():
        print("OUT:\n" + out + "\nEXP:\n" + expected)
    sys.stdout.write("")
