import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M3-d")
page = (ROOT / "course/modules/M/M3/project.html").read_text()
py = str(ROOT / ".venv/bin/python")
for lab in ["project-1", "project-2", "project-3"]:
    twin = ROOT / f"tests/labs/M3/lab-M3-{lab}.py"
    tsrc = twin.read_text()
    r = subprocess.run([py, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    print(lab, "twin exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
    # page code blocks
    secm = re.search(r'<section class="lab[^"]*" id="lab-M3-%s".*?</section>' % lab, page, re.S)
    sec = secm.group(0)
    codes = re.findall(r'<pre><code[^>]*>(.*?)</code></pre>', sec, re.S)
    print(" code blocks in section:", len(codes))
    code = html.unescape(codes[0])
    print(" page code == twin:", code.strip() == tsrc.strip())
    if code.strip() != tsrc.strip():
        import difflib
        for l in list(difflib.unified_diff(tsrc.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:30]:
            print("  ", l)
    outs = re.findall(r'<pre class="[^"]*output[^"]*"[^>]*>(.*?)</pre>|<pre><samp[^>]*>(.*?)</samp></pre>', sec, re.S)
    print(" expected-block candidates:", len(outs))
    tail = sec[sec.find("</pre>"):][:0]
    # generic: print all <pre> blocks not containing code
    pres = re.findall(r'<pre(?![^>]*data-run)[^>]*>(.*?)</pre>', sec, re.S)
    for i, p in enumerate(pres):
        ptxt = html.unescape(re.sub(r'<[^>]+>', '', p))
        if i == 0 or ptxt.strip() == "":
            pass
        print(" pre", i, "lines", ptxt.strip().count("\n") + 1)
        if ptxt.strip() and ptxt.strip() == r.stdout.strip():
            print("  EXPECTED == twin stdout: True")
    print(" twin stdout:\n" + r.stdout)
