import re, subprocess, sys, html
page = "/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/project.html"
src = open(page, encoding="utf-8").read()
blocks = re.findall(r'<section class="lab[^"]*" id="([^"]+)"[^>]*>(.*?)</section>', src, re.S)
for lab_id, body in blocks:
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    exp = html.unescape(exp.group(1)) if exp else None
    twin = f"/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/tests/labs/E3/{lab_id}.py"
    tsrc = open(twin, encoding="utf-8").read()
    print(lab_id, "page_code==twin:", code.rstrip("\n") == tsrc.rstrip("\n"))
    r = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, cwd="/tmp")
    print("exit", r.returncode, "stderr:", repr(r.stderr[:200]))
    out = r.stdout.rstrip("\n")
    print("expected==output:", exp.rstrip("\n") == out if exp else "NO EXPECTED")
    if exp and exp.rstrip("\n") != out:
        print("OUT:\n" + out)
    else:
        print(out)
    print("-----")
