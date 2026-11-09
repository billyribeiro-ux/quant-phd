import difflib
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
pairs = {"L07": "lab-M3-L07-1.py", "L08": "lab-M3-L08-1.py", "L09": "lab-M3-L09-1.py"}
for lesson, twin in pairs.items():
    page = (root / f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf-8")
    twin_path = root / "tests/labs/M3" / twin
    tw = twin_path.read_text(encoding="utf-8")
    code = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    proc = subprocess.run(
        [str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)],
        capture_output=True, text=True, cwd=str(root / "tests/labs/M3"),
    )
    out = proc.stdout
    print(f"{lesson} twin rc={proc.returncode} stderr_bytes={len(proc.stderr)} stdout_lines={out.count(chr(10))}")
    print(f"{lesson} data-run blocks={len(code)} expected blocks={len(exp)}")
    code_eq = bool(code) and html.unescape(code[0]).rstrip("\n") == tw.rstrip("\n")
    exp_eq = bool(exp) and html.unescape(exp[0]).strip("\n") == out.strip("\n")
    print(f"{lesson} page code == twin: {code_eq}; expected == twin stdout: {exp_eq}")
    if not exp_eq:
        print("".join(difflib.unified_diff(out.splitlines(True), html.unescape(exp[0]).splitlines(True))))
    if not code_eq and code:
        print("".join(difflib.unified_diff(tw.splitlines(True), html.unescape(code[0]).splitlines(True))))
