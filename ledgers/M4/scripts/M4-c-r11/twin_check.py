import html, re, sys
root = sys.argv[1]
for L in ["L08", "L09", "L10"]:
    page = open(f"{root}/course/modules/M/M4/{L}.html", encoding="utf-8").read()
    m = re.search(r'<section class="lab" id="lab-M4-%s-1".*?<code class="language-python" data-run>(.*?)</code>' % L, page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/M4/lab-M4-{L}-1.py", encoding="utf-8").read()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    out = open(f"/tmp/m4c_r11_{L}.out", encoding="utf-8").read()
    print(L, "code==twin", code.strip() == twin.strip(), "len", len(code), len(twin))
    print(L, "expected==output", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(out.strip().splitlines(), exp.strip().splitlines(), lineterm="")))
