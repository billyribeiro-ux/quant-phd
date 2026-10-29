"""Compare each project lab block in project.html with its twin and its expected output (verifier r5)."""
import html, re, sys
from pathlib import Path
root = Path("/tmp/verifyB5-E1-d")
page = (root / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"?[^>]*>(.*?)</pre>', page, flags=re.S)
print("code+expected blocks found:", len(blocks))
for code, exp in blocks:
    code_t = html.unescape(code)
    first = code_t.splitlines()[0][:60]
    # match twin by docstring first line
    for n in (1, 2, 3):
        twin = (root / f"tests/labs/E1/lab-E1-project-{n}.py").read_text(encoding="utf-8")
        if twin.strip() == code_t.strip():
            out = (root / f"ledgers/E1/scripts/E1-d-r5/lab-E1-project-{n}.out").read_text(encoding="utf-8")
            exp_t = html.unescape(exp).strip()
            print(f"lab project-{n}: code identical to twin; expected == run output: {exp_t == out.strip()}")
            break
    else:
        print("no identical twin for block starting:", repr(first), "len", len(code_t), len(twin))
