import html, re, subprocess, sys
root = "/tmp/verifyB4-M4-b"
for page, lab in [("L05", "lab-M4-L05-1"), ("L06", "lab-M4-L06-1"), ("L07", "lab-M4-L07-1")]:
    src = open(f"{root}/course/modules/M/M4/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).strip()
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/M4/{lab}.py"],
                         capture_output=True, text=True, check=True).stdout.strip()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(code_m.group(1)).strip()
    twin = open(f"{root}/tests/labs/M4/{lab}.py", encoding="utf-8").read().strip()
    print(page, "expected==run:", expected == out, "code==twin:", code == twin, "lines", len(out.splitlines()))
    if expected != out:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
