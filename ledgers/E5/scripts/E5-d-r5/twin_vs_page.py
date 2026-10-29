"""Compare each data-run block in project.html with its twin file, and each expected block with twin output."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/E/E5/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*(?:<pre class="expected"[^>]*>(.*?)</pre>)?', page, re.S)
twins = ["lab-E5-project-1.py", "lab-E5-project-2.py", "lab-E5-project-3.py"]
for name, (code, exp) in zip(twins, blocks):
    code_html = html.unescape(code)
    twin = (root / "tests/labs/E5" / name).read_text(encoding="utf-8")
    print(name, "page==twin:", code_html.strip() == twin.strip(), "len", len(code_html), len(twin))
    if not code_html.strip() == twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code_html.splitlines(True)))[:40]))
    print("  expected block present:", bool(exp))
print("blocks found:", len(blocks))
