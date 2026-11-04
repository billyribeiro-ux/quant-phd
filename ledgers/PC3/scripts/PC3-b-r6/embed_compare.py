"""Compare each PC3 slice page lab block with its twin (code) and with the twin's stdout (expected). PC3-b round 6."""
import html, re, subprocess, sys
root = sys.argv[1]
pages = {"L04": "lab-PC3-L04-1", "L05": "lab-PC3-L05-1", "L06": "lab-PC3-L06-1"}
for page, twin in pages.items():
    src = open(f"{root}/course/modules/PC/PC3/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    twin_src = open(f"{root}/tests/labs/PC3/{twin}.py", encoding="utf-8").read()
    page_code = html.unescape(code.group(1))
    print(page, "code blocks:", len(re.findall(r'data-run', src)), "expected blocks:", len(re.findall(r'class="expected"', src)))
    print(" page code == twin:", page_code.rstrip() == twin_src.rstrip(), " len", len(page_code), len(twin_src))
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/PC3/{twin}.py"],
                         capture_output=True, text=True)
    expected = html.unescape(exp.group(1))
    print(" expected == stdout:", expected.rstrip() == out.stdout.rstrip(), "rc", out.returncode, "stderr bytes", len(out.stderr))
    if expected != out.stdout:
        import difflib
        print("".join(list(difflib.unified_diff(expected.splitlines(True), out.stdout.splitlines(True)))[:40]))
