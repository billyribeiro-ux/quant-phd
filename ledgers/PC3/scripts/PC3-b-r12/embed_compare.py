"""Compare each PC3 page's lab code and expected block with its twin and the twin's real stdout.

Stdlib only. Usage: python -I embed_compare.py <checkout_root>
"""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
out = root / "ledgers/PC3/scripts/PC3-b-r12/out"
out.mkdir(parents=True, exist_ok=True)
pages = {"L04": "lab-PC3-L04-1", "L05": "lab-PC3-L05-1", "L06": "lab-PC3-L06-1"}
ok_all = True
for page, lab in pages.items():
    text = (root / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/PC3/{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="%s".*?</section>' % lab, text, re.S)
    assert sec, page
    s = sec.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)
    exp = html.unescape(re.sub(r"<[^>]+>", "", exp))
    r = subprocess.run(
        [str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)],
        capture_output=True, text=True, cwd=str(root / "tests/labs/PC3"),
    )
    (out / f"twin_{lab}.stdout").write_text(r.stdout, encoding="utf-8")
    (out / f"twin_{lab}.stderr").write_text(r.stderr, encoding="utf-8")
    code_eq = code.strip("\n") == twin.strip("\n")
    exp_eq = exp.strip("\n") == r.stdout.strip("\n")
    print(page, lab, "code==twin", code_eq, "expected==stdout", exp_eq,
          "exit", r.returncode, "stderr_bytes", len(r.stderr.encode()), "expected_lines", len(exp.strip("\n").splitlines()),
          "stdout_lines", len(r.stdout.strip("\n").splitlines()))
    if not (code_eq and exp_eq and r.returncode == 0 and not r.stderr):
        ok_all = False
        if not code_eq:
            print("  code diff first mismatch lines:")
            a, b = code.strip("\n").splitlines(), twin.strip("\n").splitlines()
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print("   ", i + 1, repr(x)[:120], "|", repr(y)[:120])
                    break
print("embed_compare", "PASS" if ok_all else "FAIL")
