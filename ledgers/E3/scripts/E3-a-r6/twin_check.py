import html, re, subprocess, sys, os
root = sys.argv[1]
ok_all = True
for L in ["L01", "L02", "L03"]:
    page = open(os.path.join(root, f"course/modules/E/E3/{L}.html"), encoding="utf-8").read()
    twin_path = os.path.join(root, f"tests/labs/E3/lab-E3-{L}-1.py")
    twin = open(twin_path, encoding="utf-8").read()
    codes = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_ok = len(codes) == 1 and html.unescape(codes[0]) == twin.rstrip("\n")
    r = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True)
    exp_ok = len(expected) == 1 and html.unescape(expected[0]) == r.stdout.rstrip("\n")
    print(L, "codes", len(codes), "code==twin(modulo final newline)", code_ok, "expected==stdout", exp_ok, "exit", r.returncode, "stderr", repr(r.stderr[:200]))
    ok_all &= code_ok and exp_ok and r.returncode == 0
print("ALL", ok_all)
