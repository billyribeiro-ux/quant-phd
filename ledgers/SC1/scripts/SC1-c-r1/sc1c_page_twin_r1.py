import html, re, subprocess, sys, pathlib, os
ROOT = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
labs = {
    "L07": ("course/modules/SC/SC1/L07.html", "tests/labs/SC1/lab-SC1-L07-1.py"),
    "L08": ("course/modules/SC/SC1/L08.html", "tests/labs/SC1/lab-SC1-L08-1.py"),
}
for k, (page, twin) in labs.items():
    p = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', p, re.S)
    code = html.unescape(m.group(1))
    tw = (ROOT / twin).read_text(encoding="utf-8")
    print(k, "page_code_equals_twin_after_rstrip:", code.rstrip("\n") == tw.rstrip("\n"), "page_lines", m.group(1).count("\n"), "twin_lines", tw.count("\n"))
    # run twin isolated
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / twin)], cwd="/tmp", capture_output=True)
    (OUT / f"{k}_stdout.txt").write_bytes(r.stdout)
    print(k, "twin_exit", r.returncode, "stderr_bytes", len(r.stderr))
    em = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', p[m.end():], re.S)
    exp = html.unescape(em.group(1))
    print(k, "expected_equals_stdout:", exp.rstrip("\n") == r.stdout.decode("utf-8").rstrip("\n"), "expected_lines", exp.count("\n"), "stdout_lines", r.stdout.decode().count("\n"))
    if exp.rstrip("\n") != r.stdout.decode("utf-8").rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), r.stdout.decode().splitlines(), lineterm="")))
