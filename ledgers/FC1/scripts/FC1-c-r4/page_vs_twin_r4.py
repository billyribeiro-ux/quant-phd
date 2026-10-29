import html, re, sys, pathlib, difflib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
labs = re.findall(r'id="(lab-FC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
for lid, code in labs:
    code = html.unescape(code)
    twin = (root / f"tests/labs/FC1/{lid}.py").read_text(encoding="utf-8")
    d = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))
    print(lid, "diff lines:", len(d)); print("\n".join(d[:30]))
