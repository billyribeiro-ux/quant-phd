import html, re, subprocess, sys, difflib
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX2-c"
page = open(f"{ROOT}/course/modules/LX/LX2/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("run blocks", len(blocks), "expected blocks", len(expected))
ok = True
for n in (1, 2, 3):
    code = html.unescape(blocks[n - 1])
    twin = open(f"{ROOT}/tests/labs/LX2/lab-LX2-project-{n}.py", encoding="utf-8").read()
    if code.strip() == twin.strip():
        print(f"lab {n}: page code == twin (exact)")
    else:
        d = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))
        print(f"lab {n}: page code differs from twin, {len(d)} diff lines")
        print("\n".join(d[:60]))
        ok = False
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/LX2/lab-LX2-project-{n}.py"],
                         capture_output=True, text=True).stdout
    exp = html.unescape(expected[n - 1])
    print(f"lab {n}: expected block == twin stdout: {exp.strip() == out.strip()}")
    ok = ok and exp.strip() == out.strip()
print("ALL", ok)
