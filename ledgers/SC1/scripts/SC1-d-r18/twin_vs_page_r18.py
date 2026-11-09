"""Compare each project lab's page code block with its twin file (tests/labs/SC1). Prints the diff lines only.
Usage: python3 -I twin_vs_page_r18.py <checkout root>"""
import difflib
import html
import re
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
for lab in ("lab-SC1-project-1", "lab-SC1-project-2", "lab-SC1-project-3"):
    sec = re.search(rf'<section[^>]*id="{lab}".*?</section>', page, re.S).group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{root}/tests/labs/SC1/{lab}.py", encoding="utf-8").read()
    page_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    print(f"== {lab}: page lines {len(page_lines)}, twin lines {len(twin_lines)}")
    for line in difflib.unified_diff(twin_lines, page_lines, "twin", "page", lineterm="", n=0):
        print(line)
