import html, re, subprocess, sys
root = sys.argv[1]
for lid in ("L07", "L08", "L09"):
    page = open(f"{root}/course/modules/E/E1/{lid}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    run = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/E1/lab-E1-{lid}-1.py"],
                         capture_output=True, text=True)
    print(lid, "stderr", len(run.stderr), "rc", run.returncode,
          "expected==run:", expected.strip() == run.stdout.strip(), "lines", len(expected.strip().splitlines()), len(run.stdout.strip().splitlines()))
    if expected.strip() != run.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(run.stdout.strip().splitlines(), expected.strip().splitlines(), lineterm="")))
    # also the code block
    cm = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(cm.group(1))
    twin = open(f"{root}/tests/labs/E1/lab-E1-{lid}-1.py", encoding="utf-8").read()
    print(lid, "page code == twin:", code.strip() == twin.strip(), len(code), len(twin))
