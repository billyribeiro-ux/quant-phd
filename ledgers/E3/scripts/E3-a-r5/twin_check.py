import html, re, subprocess, sys
pairs = {"L01": "tests/labs/E3/lab-E3-L01-1.py", "L02": "tests/labs/E3/lab-E3-L02-1.py", "L03": "tests/labs/E3/lab-E3-L03-1.py"}
root = sys.argv[1]
for page, twin in pairs.items():
    h = open(f"{root}/course/modules/E/E3/{page}.html", encoding="utf-8").read()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', h, re.S)
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    eq = [html.unescape(b).rstrip("\n") == tw.rstrip("\n") for b in blocks]
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', h, re.S)
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/{twin}"], capture_output=True, text=True).stdout
    print(page, "code blocks", len(blocks), "equal twin", eq, "expected blocks", len(exp),
          "expected==stdout", [html.unescape(e).strip() == out.strip() for e in exp])
