"""Compare each L07/L08 page's data-run code block with its twin, and each expected block with twin stdout."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
for page, twin in (("L07", "lab-SC1-L07-1"), ("L08", "lab-SC1-L08-1")):
    text = open(f"{ROOT}/course/modules/SC/SC1/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_src = open(f"{ROOT}/tests/labs/SC1/{twin}.py", encoding="utf-8").read()
    print(page, "code chars", len(code), "twin chars", len(twin_src), "equal exactly:", code == twin_src,
          "equal after rstrip:", code.rstrip() == twin_src.rstrip())
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/SC1/{twin}.py"],
                         capture_output=True, text=True)
    print(page, "twin exit", run.returncode, "stderr chars", len(run.stderr))
    print(page, "expected == stdout exactly:", expected == run.stdout,
          "| after rstrip:", expected.rstrip() == run.stdout.rstrip())
    if expected.rstrip() != run.stdout.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), run.stdout.splitlines(), lineterm="")))
    # any other code block or expected block on the page?
    print(page, "data-run blocks:", len(re.findall(r"data-run", text)), "expected blocks:", len(re.findall(r'class="expected"', text)))
