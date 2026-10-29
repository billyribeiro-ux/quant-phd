import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
for lab, page in (("L04", "L04"), ("L05", "L05"), ("L06", "L06")):
    src = (root / f"course/modules/E/E5/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/E5/lab-E5-{lab}-1.py").read_text(encoding="utf-8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(re.sub(r'<[^>]+>', '', exp.group(1))) if exp else None
    print(lab, "code_equal_twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), n=0))[:40]))
    out = open(root / f"ledgers/E5/scripts/E5-b-r12/twin_{lab}_out.txt", "w")
    import subprocess
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E5/lab-E5-{lab}-1.py")], capture_output=True, text=True)
    print(lab, "expected_equal_output:", expected is not None and expected.strip() == r.stdout.strip(), "rc", r.returncode)
