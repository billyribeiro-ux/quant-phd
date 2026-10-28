import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
py = str(root / ".venv/bin/python")
for n in range(7, 13):
    tw = root / f"tests/labs/M2/lab-M2-L{n:02d}-1.py"
    page = (root / f"course/modules/M/M2/L{n:02d}.html").read_text()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(m.group(1))
    r = subprocess.run([py, "-I", "-W", "error", str(tw)], capture_output=True, text=True, timeout=120)
    ok = r.stdout.rstrip("\n") == exp.rstrip("\n")
    print(f"L{n:02d} rc={r.returncode} stderr={r.stderr.strip()[:200]!r} embed_match={ok} lines={len(r.stdout.splitlines())}")
    if not ok:
        import difflib
        print("\n".join(list(difflib.unified_diff(exp.splitlines(), r.stdout.splitlines(), lineterm=''))[:20]))
    # also code embedded equals twin
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    print("   code_match_twin:", code.strip() == tw.read_text().strip())
