import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
pairs = [
    ("course/modules/M/M4/project.html", "tests/labs/M4/lab-M4-project-1.py", "lab-M4-project-1"),
    ("course/modules/M/M4/project.html", "tests/labs/M4/lab-M4-project-2.py", "lab-M4-project-2"),
    ("course/modules/M/M4/project.html", "tests/labs/M4/lab-M4-project-3.py", "lab-M4-project-3"),
    ("course/modules/M/M4/L04.html", "tests/labs/M4/lab-M4-L04-1.py", "lab-M4-L04-1"),
]
for page, twin, label in pairs:
    text = (root / page).read_text(encoding="utf-8")
    # find the lab's <pre><code ... data-run> block that follows the section id
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text[text.find(label) if label in text else 0:], re.S)
    code = html.unescape(m.group(1)) if m else None
    tw = (root / twin).read_text(encoding="utf-8")
    if code is None:
        print(label, "NO BLOCK FOUND")
        continue
    print(label, "page==twin:", code == tw, "len page", len(code), "len twin", len(tw))
    if code != tw:
        import difflib
        for line in list(difflib.unified_diff(tw.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:30]:
            print("   ", line)
