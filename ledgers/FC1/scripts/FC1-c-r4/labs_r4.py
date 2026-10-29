"""Round 4 check: page lab code equals twin; twin output equals expected block; blanks as Lab 2 states."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-FC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lid, code, expected in labs:
    code = html.unescape(code)
    twin = (root / f"tests/labs/FC1/{lid}.py").read_text(encoding="utf-8")
    print(lid, "page==twin:", code == twin, "blanks:", code.count("___"))
    if code.count("___") == 0 or lid != "lab-FC1-project-2":
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC1/{lid}.py")], capture_output=True, text=True)
        print("  exit", r.returncode, "stderr bytes", len(r.stderr), "stdout==expected:", r.stdout.strip() == html.unescape(expected).strip())
    else:
        filled = code.replace("(1 + y) ** ___", "(1 + y) ** period").replace("(settlement_day, ___)", "(settlement_day, -side * quantity * price_cents)")
        print("  filled page == twin:", filled == twin)
        pathlib.Path("/tmp/fc1c4/lab2_filled.py").write_text(filled, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", "/tmp/fc1c4/lab2_filled.py"], capture_output=True, text=True)
        print("  filled exit", r.returncode, "stderr", len(r.stderr), "stdout==expected:", r.stdout.strip() == html.unescape(expected).strip())
