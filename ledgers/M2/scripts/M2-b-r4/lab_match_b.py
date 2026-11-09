"""Compare the embedded lab code and expected block of each slice-b page with its twin and with a fresh run."""
import html, re, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS4-M2-b")
PY = str(ROOT / ".venv/bin/python")
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    page = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python"[^>]*>(.*?)</code></pre>', page, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin_path = ROOT / f"tests/labs/M2/lab-M2-{L}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = html.unescape(codes[0]) if codes else ""
    same = code.rstrip("\n") == twin.rstrip("\n")
    diffs = [] if same else [i for i, (a, b) in enumerate(zip(code.splitlines(), twin.splitlines())) if a != b]
    out = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    exp = html.unescape(expected[0]) if expected else ""
    exp_same = exp.rstrip("\n") == out.stdout.rstrip("\n")
    print(f"{L}: code_blocks={len(codes)} expected_blocks={len(expected)} page_code_eq_twin={same} "
          f"first_diff_lines={diffs[:5]} run_exit={out.returncode} expected_eq_output={exp_same} "
          f"out_lines={len(out.stdout.splitlines())} stderr={out.stderr.strip()[:200]!r}")
    if not exp_same:
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.stdout.splitlines(), lineterm="")))
