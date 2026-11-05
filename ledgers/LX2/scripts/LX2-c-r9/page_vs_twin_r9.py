import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-LX2-project-{n}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/LX2/lab-LX2-project-{n}.py").read_text(encoding="utf-8")
    code_lines = code.rstrip("\n").split("\n"); twin_lines = twin.rstrip("\n").split("\n")
    diffs = [(i + 1, a, b) for i, (a, b) in enumerate(zip(code_lines, twin_lines)) if a != b]
    print(f"lab {n}: page code lines {len(code_lines)}, twin lines {len(twin_lines)}, differing lines {len(diffs)}")
    for d in diffs: print("   ", d)
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/LX2/lab-LX2-project-{n}.py")], capture_output=True, text=True)
    print(f"  twin exit {r.returncode}; stderr {r.stderr.strip()!r}")
    out = r.stdout.rstrip("\n"); e = exp.rstrip("\n")
    print(f"  stdout == expected block: {out == e} (out {len(out.splitlines())} lines, expected {len(e.splitlines())} lines)")
    open(f"{sys.argv[2]}/twin_out_lab{n}.txt", "w").write(r.stdout)
