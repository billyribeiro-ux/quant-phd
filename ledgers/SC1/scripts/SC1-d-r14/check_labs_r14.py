"""Compare each project lab's code and expected block on project.html with its twin and with the twin's stdout.

Tags are stripped before entities are decoded, so that a literal less-than sign is not read as a tag.
Lab 2 is a completion problem: its page code keeps the blanks, so the page-vs-twin code diff is expected there.
"""
import difflib
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
page = open(f"{ROOT}/course/modules/SC/SC1/project.html", encoding="utf-8").read()


def text_of(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


ok = True
for i in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-SC1-project-{i}".*?</section>', page, re.S).group(0)
    code = text_of(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = text_of(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = open(f"{ROOT}/tests/labs/SC1/lab-SC1-project-{i}.py", encoding="utf-8").read()
    same_code = code.strip() == twin.strip()
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/SC1/lab-SC1-project-{i}.py"],
        capture_output=True, text=True, cwd="/tmp",
    ).stdout
    same_out = expected.strip() == out.strip()
    print(f"lab {i}: page code == twin: {same_code}; expected == twin stdout: {same_out}")
    if not same_code:
        print("\n".join(list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]))
    if not same_out:
        print("EXPECTED:\n" + expected + "\nSTDOUT:\n" + out)
    ok = ok and same_out and (same_code or i == 2)
print("ALL OK" if ok else "MISMATCH")
