import sys, re, html, subprocess
# compare page lab code block and expected block with the twin and with the live output
page, twin, lab = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(page, encoding="utf-8").read()
sec = s[s.index(f'id="{lab}"'):]
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
code = html.unescape(code)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
exp = html.unescape(re.sub(r"<[^>]+>", "", exp))
twin_src = open(twin, encoding="utf-8").read()
print("code == twin (strip trailing ws):", code.rstrip() == twin_src.rstrip())
if code.rstrip() != twin_src.rstrip():
    import difflib
    print("\n".join(list(difflib.unified_diff(twin_src.rstrip().splitlines(), code.rstrip().splitlines(), lineterm=""))[:40]))
out = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True).stdout
print("expected == live output:", exp.rstrip() == out.rstrip())
if exp.rstrip() != out.rstrip():
    import difflib
    print("\n".join(difflib.unified_diff(out.rstrip().splitlines(), exp.rstrip().splitlines(), lineterm="")))
