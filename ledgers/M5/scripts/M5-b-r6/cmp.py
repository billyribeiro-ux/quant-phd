import re, subprocess, sys, html, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-M5-b")
for lid in ["L05","L06","L07"]:
    src = (root/f"course/modules/M/M5/{lid}.html").read_text()
    i = src.find(f'id="lab-M5-{lid}-1"')
    j = src.find('<pre class="expected"', i)
    k = src.find('</pre>', j)
    exp = html.unescape(src[src.find('>', j)+1:k])
    c0 = src.find('<code', i); c0 = src.find('>', c0)+1; c1 = src.find('</code>', c0)
    code_html = html.unescape(src[c0:c1])
    twin = (root/f"tests/labs/M5/lab-M5-{lid}-1.py").read_text()
    print(lid, "code==twin:", code_html.rstrip("\n")==twin.rstrip("\n"), flush=True)
    try:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root/f"tests/labs/M5/lab-M5-{lid}-1.py")], capture_output=True, text=True, cwd="/private/tmp/m5b6", timeout=60)
    except subprocess.TimeoutExpired:
        print(lid, "TIMEOUT", flush=True); continue
    print(lid, "rc", r.returncode, "stderr", repr(r.stderr[:200]), flush=True)
    print(lid, "expected==output:", exp.strip()==r.stdout.strip(), flush=True)
    if exp.strip()!=r.stdout.strip():
        print("EXP:\n"+exp); print("OUT:\n"+r.stdout, flush=True)
