"""Compare each project-page lab code block (data-run) with its twin file, and each expected block with the twin's output."""
import html, pathlib, re, subprocess, sys
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-E1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in sections:
    code = html.unescape(code)
    twin = (root / f"tests/labs/E1/{lab_id.replace('lab-', 'lab-')}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E1/{lab_id}.py")], capture_output=True, text=True).stdout
    exp = html.unescape(expected).strip()
    print(lab_id, "code==twin:", same, "| expected==output:", exp == out.strip(), "| len", len(code), len(twin))
    if not same:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    if exp != out.strip():
        import difflib
        print("".join(list(difflib.unified_diff(out.strip().splitlines(True), exp.splitlines(True), "output", "expected"))[:40]))
