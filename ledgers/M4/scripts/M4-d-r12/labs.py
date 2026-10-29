import re, html, subprocess, sys
root = "/Users/billyribeiro/.fanout/wt/verifyB12-M4-d/"
page = open(root + "course/modules/M/M4/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("found lab blocks:", len(blocks))
for idx, (code, expected) in enumerate(blocks, 1):
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = open(root + f"tests/labs/M4/lab-M4-project-{idx}.py", encoding="utf-8").read()
    print(f"lab {idx}: page code == twin: {code == twin} (len page {len(code)} twin {len(twin)})")
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), n=0))[:40]))
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", "import sys; sys.argv=['x']; exec(compile(open(sys.argv[0]).read(),'x','exec'))"], capture_output=True)
    run = subprocess.run([sys.executable, "-I", "-W", "error", root + f"tests/labs/M4/lab-M4-project-{idx}.py"], capture_output=True, text=True, cwd="/tmp/M4-d-r12-scratch")
    print("exit", run.returncode, "stderr:", run.stderr.strip()[:200])
    print("stdout == expected:", run.stdout.strip() == expected.strip())
    if run.stdout.strip() != expected.strip():
        print("OUT:\n" + run.stdout); print("EXP:\n" + expected)
