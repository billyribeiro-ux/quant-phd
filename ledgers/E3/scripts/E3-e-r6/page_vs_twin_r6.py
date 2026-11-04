import difflib, html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD6-E3-e")
page = (root / "course/modules/E/E3/project.html").read_text()
for n in (1, 2, 3):
    m = re.search(r'<section class="lab[^"]*" id="lab-E3-project-%d".*?</section>' % n, page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    twin = (root / ("tests/labs/E3/lab-E3-project-%d.py" % n)).read_text()
    if n == 2:
        # the completion blanks: replace each ___ line by the twin's line in the same position
        twin_lines = twin.splitlines()
        page_lines = code.splitlines()
        blanks = [i for i, l in enumerate(page_lines) if l.strip() == "return ___"]
        twin_ret = [l for l in twin_lines if l.strip().startswith("return -math")]
        filled = list(page_lines)
        for i, t in zip(blanks, twin_ret):
            filled[i] = t
        print("lab 2 blanks:", len(blanks), "twin return lines:", len(twin_ret))
        print("lab 2 page with blanks filled == twin:", "\n".join(filled).strip() == twin.strip())
    else:
        print("lab", n, "page code == twin:", code.strip() == twin.strip())
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / ("tests/labs/E3/lab-E3-project-%d.py" % n))], capture_output=True, text=True).stdout
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    expected = html.unescape(exp.group(1)).strip()
    print("lab", n, "expected block == twin output:", expected == out.strip())
    if expected != out.strip():
        print("\n".join(difflib.unified_diff(out.strip().splitlines(), expected.splitlines(), lineterm="", fromfile="output", tofile="expected")))
