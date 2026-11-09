"""Round 17: compare each project lab's page code and expected block with its twin, and run the twin alone.

Usage: python -I twin_vs_page_r17.py <repo_root>
Prints one line per lab: code-equal flag, expected-equal flag (against the twin's own output), and the twin exit code.
"""
import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/PC/PC3/project.html", encoding="utf-8").read()
py = f"{root}/.venv/bin/python"
for n in (1, 2, 3):
    sec = re.search(rf'<section[^>]*id="lab-PC3-project-{n}"[^>]*>(.*?)</section>', page, re.S)
    body = sec.group(1)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin_path = f"{root}/tests/labs/PC3/lab-PC3-project-{n}.py"
    twin = open(twin_path, encoding="utf-8").read()
    code_equal = code.strip("\n") == twin.strip("\n")
    run = subprocess.run([py, "-I", "-W", "error", twin_path], capture_output=True, text=True, timeout=60)
    out_equal = run.stdout.strip() == expected.strip()
    print(f"lab-PC3-project-{n}: page_code==twin {code_equal}; expected==twin_output {out_equal}; "
          f"twin_exit {run.returncode}; stderr_bytes {len(run.stderr)}")
    if not code_equal:
        import difflib
        for line in difflib.unified_diff(twin.strip("\n").splitlines(), code.strip("\n").splitlines(),
                                         "twin", "page", lineterm="", n=0):
            print("   ", line)
    if not out_equal:
        print("    twin output:", run.stdout.strip()[:300])
