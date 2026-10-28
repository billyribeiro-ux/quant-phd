import html, re, subprocess, sys
root = sys.argv[1]
for lab in ["L07", "L08"]:
    page = open(f"{root}/course/modules/AC/AC4/{lab}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page[page.index(f'id="lab-AC4-{lab}-1"'):], re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page[page.index(f'id="lab-AC4-{lab}-1"'):], re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py"], capture_output=True, text=True).stdout
    print(lab, "code==twin:", code.strip() == twin.strip(), "expected==stdout:", exp.strip() == out.strip(), len(exp), len(out))
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
