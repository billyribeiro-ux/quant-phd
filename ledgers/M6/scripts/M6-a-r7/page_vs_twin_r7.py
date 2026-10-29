import re, html, subprocess, sys
root = "/Users/billyribeiro/.fanout/wt/verifyC7-M6-a"
for n in range(1, 5):
    page = open(f"{root}/course/modules/M/M6/L0{n}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/M6/lab-M6-L0{n}-1.py", encoding="utf-8").read()
    code_m = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/M6/lab-M6-L0{n}-1.py"], capture_output=True, text=True).stdout
    code_ok = [html.unescape(c).strip() == twin.strip() for c in code_m]
    exp_ok = [html.unescape(e).strip() == out.strip() for e in exp_m]
    print(f"L0{n}: code blocks={len(code_m)} equal_twin={code_ok} expected blocks={len(exp_m)} equal_output={exp_ok}")
