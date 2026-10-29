import html, re, subprocess, sys
root = sys.argv[1]
for n in ("01", "02", "03"):
    page = open(f"{root}/course/modules/E/E5/L{n}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/E5/lab-E5-L{n}-1.py", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    print(f"L{n} code==twin exact:", code == twin, "| modulo final newline:", code.rstrip("\n") == twin.rstrip("\n"), len(code), len(twin))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    out = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/E5/lab-E5-L{n}-1.py"],
                         capture_output=True, text=True).stdout
    print(f"L{n} expected==output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
