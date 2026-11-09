"""Compare each project lab's page code block with its twin, and the page's expected block with the twin's output.
Usage: twin_vs_page_r16.py <checkout root>. Run with the checkout's .venv python, not -I (it runs the twins with -I -W error itself)."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(blocks), "expected blocks:", len(expected))
for i, (code, exp) in enumerate(zip(blocks, expected), start=1):
    page_code = html.unescape(code)
    twin = open(f"{root}/tests/labs/SC1/lab-SC1-project-{i}.py", encoding="utf-8").read()
    same = page_code.rstrip("\n") == twin.rstrip("\n")
    print(f"lab {i}: page code == twin: {same} (page {len(page_code)} chars, twin {len(twin)} chars)")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), page_code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    r = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/SC1/lab-SC1-project-{i}.py"],
                       capture_output=True, text=True, cwd="/tmp/sc1d-r16")
    out = r.stdout.rstrip("\n")
    exp_text = html.unescape(exp).rstrip("\n")
    print(f"lab {i}: twin exit {r.returncode}; stderr {r.stderr.strip()[:200]!r}")
    print(f"lab {i}: expected block == twin output: {exp_text == out}")
    if exp_text != out:
        for a, b in zip(exp_text.splitlines(), out.splitlines()):
            if a != b:
                print("   expected:", a)
                print("   output  :", b)
