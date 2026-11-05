"""Compare each E4 project lab's page code (data-run block) with its twin, and its expected block with the twin's output."""
import html, re, subprocess, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d"
page = open(f"{ROOT}/course/modules/E/E4/project.html", encoding="utf-8").read()
for n in (1, 2, 3):
    lab = f"lab-E4-project-{n}"
    m = re.search(r'id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = open(f"{ROOT}/tests/labs/E4/{lab}.py", encoding="utf-8").read()
    print(lab, "page code == twin:", code.strip() == twin.strip(), "| code chars", len(code), len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
    out = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/tests/labs/E4/{lab}.py"], capture_output=True, text=True).stdout
    print(lab, "expected block == twin output:", expected.strip() == out.strip())
    if expected.strip() != out.strip():
        import difflib
        print("".join(list(difflib.unified_diff(out.splitlines(True), expected.splitlines(True), "output", "expected"))[:40]))
