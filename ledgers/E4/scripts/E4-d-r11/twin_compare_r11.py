"""Compare each E4 project lab's page code block with its twin (tests/labs/E4). Usage: python3 -I twin_compare_r11.py <root>."""
import html
import re
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/E/E4/project.html", encoding="utf-8").read()
for n in (1, 2, 3):
    sec_start = page.index(f'id="lab-E4-project-{n}"')
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page[sec_start:], re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/E4/lab-E4-project-{n}.py", encoding="utf-8").read()
    print(f"lab-E4-project-{n}: page code len {len(code)} twin len {len(twin)} equal={code.strip() == twin.strip()}")
    if code.strip() != twin.strip():
        import difflib
        for line in list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:30]:
            print("   ", line)
