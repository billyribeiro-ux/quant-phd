import html, re, subprocess, sys, pathlib
page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
twin_dir = pathlib.Path(sys.argv[2])
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-M7-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    expected = html.unescape(expected).rstrip("\n")
    twin = (twin_dir / f"{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.strip() == twin.strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", code], capture_output=True, text=True)
    got = out.stdout.rstrip("\n")
    print(lab_id, "page_code==twin:", same_code, "exit:", out.returncode, "stdout==expected:", got == expected, "stderr:", out.stderr.strip()[:200])
    if got != expected:
        print("GOT:\n" + got + "\nEXPECTED:\n" + expected)
