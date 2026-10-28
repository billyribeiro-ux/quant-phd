import html, re, subprocess, sys
root = "/tmp/verifyC1-FC2-a"
for lab, page in [("1", "L01"), ("2", "L02"), ("3", "L03")]:
    src = open(f"{root}/course/modules/FC/FC2/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).strip()
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/FC2/lab-FC2-L0{lab}-1.py"], capture_output=True, text=True).stdout.strip()
    print(page, "expected == actual:", expected == out)
    if expected != out:
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
