"""Compare each E1 slice-a lab twin with the code and expected block embedded in its page (round 2)."""
import html, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
for lab, page in [("lab-E1-L01-1", "L01"), ("lab-E1-L02-1", "L02"), ("lab-E1-L03-1", "L03")]:
    text = (root / f"course/modules/E/E1/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin = (root / f"tests/labs/E1/{lab}.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E1/{lab}.py")],
                         capture_output=True, text=True)
    print(lab, "code==twin:", code.strip() == twin.strip(), "stdout==expected:", run.stdout.strip() == expected.strip(),
          "rc:", run.returncode, "stderr:", repr(run.stderr[:200]))
