import html, re, subprocess, sys, pathlib
D = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b")
out = []
for page, twin in [("L04", "lab-FC1-L04-1.py"), ("L05", "lab-FC1-L05-1.py")]:
    text = (D / "course/modules/FC/FC1" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    tw = (D / "tests/labs/FC1" / twin).read_text(encoding="utf-8")
    same = code.rstrip("\n") == tw.rstrip("\n")
    out.append(f"{page} page code == twin (trailing newlines aside): {same}; code lines {code.count(chr(10))}, twin lines {tw.count(chr(10))}; page code starts at line {text[:m.start()].count(chr(10))+1}")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(D / "tests/labs/FC1" / twin)], capture_output=True, text=True, cwd="/tmp")
    out.append(f"{page} twin rc={r.returncode} stderr_bytes={len(r.stderr)}")
    out.append(f"{page} expected == output (trailing newline aside): {expected.rstrip(chr(10)) == r.stdout.rstrip(chr(10))}; expected lines {expected.count(chr(10))+1}, output lines {r.stdout.count(chr(10))}; expected starts line {text[:e.start()].count(chr(10))+1}")
    if expected.rstrip("\n") != r.stdout.rstrip("\n"):
        out.append("DIFF:\n" + "\n".join(__import__('difflib').unified_diff(expected.splitlines(), r.stdout.splitlines(), lineterm="")))
print("\n".join(out))
