import html, re, sys, subprocess, difflib
from pathlib import Path
root = Path(sys.argv[1])
for lab in ["L19", "L20", "L21"]:
    txt = (root / f"course/modules/M/M2/{lab}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M2/lab-M2-{lab}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', txt, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', txt, re.S)
    expected = html.unescape(e.group(1))
    print(lab, "code_equals_twin", code.strip() == twin.strip(), len(code.splitlines()), len(twin.splitlines()))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-{lab}-1.py")], capture_output=True, text=True).stdout
    print(lab, "expected_equals_output_exact", expected.strip() == out.strip())
    if expected.strip() != out.strip():
        print("\n".join(difflib.unified_diff(out.strip().splitlines(), expected.strip().splitlines(), lineterm="")))
