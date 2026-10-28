"""Compare each L07/L08 embedded lab code block and expected block with the twin file and the live run."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
py = sys.executable
for lab in ("L07", "L08"):
    page = open(f"{root}/course/modules/AC/AC4/{lab}.html", encoding="utf-8").read()
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py", encoding="utf-8").read()
    print(lab, "embedded code == twin:", code.strip() == twin.strip(), len(code), len(twin))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run = subprocess.run([py, "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py"],
                         capture_output=True, text=True).stdout
    print(lab, "expected == live output:", exp.strip() == run.strip())
    if exp.strip() != run.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), run.strip().splitlines(), lineterm="")))
