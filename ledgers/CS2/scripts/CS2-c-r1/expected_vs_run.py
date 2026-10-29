"""Compare each lab's embedded expected output on L09-L11 with a fresh run of its twin (verifier round 1)."""
import html, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
for lesson, lab in (("L09", "lab-CS2-L09-1"), ("L10", "lab-CS2-L10-1"), ("L11", "lab-CS2-L11-1")):
    page = (root / "course/modules/CS/CS2" / f"{lesson}.html").read_text()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)).strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/CS2" / f"{lab}.py")],
                         capture_output=True, text=True, check=True).stdout.strip()
    print(lesson, "expected == run:", expected == run)
    # twin text vs lab code in page
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1)
    twin = (root / "tests/labs/CS2" / f"{lab}.py").read_text()
    print(lesson, "page code == twin:", html.unescape(code).rstrip("\n") == twin.rstrip("\n"))
