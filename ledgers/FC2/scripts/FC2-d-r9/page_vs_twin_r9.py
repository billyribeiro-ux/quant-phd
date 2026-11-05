"""Compare each project.html runnable code block with its lab twin, and each expected block with the twin's stdout."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/FC/FC2/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
print("runnable python blocks on page:", len(blocks))
for n in (1, 2, 3):
    twin = open(f"{root}/tests/labs/FC2/lab-FC2-project-{n}.py", encoding="utf-8").read()
    # find the block whose unescaped text starts with the twin's docstring first line
    first = twin.splitlines()[0]
    cands = [html.unescape(b) for b in blocks if html.unescape(b).startswith(first)]
    print(f"lab {n}: candidate blocks {len(cands)}")
    for c in cands:
        t_lines = twin.rstrip("\n").splitlines()
        c_lines = c.rstrip("\n").splitlines()
        diffs = [(i + 1, a, b) for i, (a, b) in enumerate(zip(t_lines, c_lines)) if a != b]
        if len(t_lines) != len(c_lines):
            diffs.append(("len", len(t_lines), len(c_lines)))
        print(f"  lines differing from twin: {len(diffs)}", [d[0] for d in diffs][:10])
        for d in diffs[:5]:
            print("   ", str(d)[:200])
    # expected block: the page's interpretation block follows; print the stdout of the twin for comparison
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/FC2/lab-FC2-project-{n}.py"],
                         capture_output=True, text=True, cwd="/tmp")
    print(f"  twin rc={out.returncode} stderr_bytes={len(out.stderr.encode())} stdout_lines={len(out.stdout.splitlines())}")
