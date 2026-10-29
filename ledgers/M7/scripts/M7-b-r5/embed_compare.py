"""Compare each slice lab page's code and expected block with its twin and with a fresh run."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in ("04", "05", "06"):
    page = (root / f"course/modules/M/M7/L{n}.html").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1)
    code = html.unescape(code)
    twin = (root / f"tests/labs/M7/lab-M7-L{n}-1.py").read_text(encoding="utf-8")
    print(f"L{n} code == twin:", code.rstrip("\n") == twin.rstrip("\n"), len(code), len(twin))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M7/lab-M7-L{n}-1.py")],
                         capture_output=True, text=True).stdout
    print(f"L{n} expected == run output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
