import html, re, sys, difflib
root = sys.argv[1]
for page in ["L04","L05","L06"]:
    src = open(f"{root}/course/modules/M/M3/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, flags=re.S)
    code_page = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/M3/lab-M3-{page}-1.py", encoding="utf-8").read()
    print(page, "len page", len(code_page), "len twin", len(twin), "equal_after_strip", code_page.strip()==twin.strip())
    for line in difflib.unified_diff(twin.splitlines(), code_page.splitlines(), "twin", "page", lineterm="", n=0):
        print(line)
