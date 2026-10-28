"""Compare each lab twin's code and embedded expected output with the page and with a fresh run."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = sys.argv[2:]
for page in pages:
    text = (root / "course/modules/M/M4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-M4-(L\d\d)-1".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    lab_id = m.group(1)
    code = html.unescape(m.group(2))
    expected = html.unescape(m.group(3))
    twin = (root / f"tests/labs/M4/lab-M4-{lab_id}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/lab-M4-{lab_id}-1.py")],
                         capture_output=True, text=True, timeout=60)
    print(page, "code==twin:", code.strip() == twin.strip(), "expected==run:", expected.strip() == run.stdout.strip(),
          "rc", run.returncode, "stderr_len", len(run.stderr))
    if expected.strip() != run.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), run.stdout.strip().splitlines(), lineterm="")))
