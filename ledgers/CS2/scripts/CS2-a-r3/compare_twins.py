# Compare each page's embedded code and expected block with its lab twin and with the twin's captured output.
import html, re, sys
base = "/Users/billyribeiro/.fanout/wt/verifyS3-CS2-a"
out_dir = "/tmp/cs2a_r3"
for lab, page in [("L01", "L01"), ("L02", "L02"), ("L03", "L03"), ("L04", "L04")]:
    txt = open(f"{base}/course/modules/CS/CS2/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', txt, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{base}/tests/labs/CS2/lab-CS2-{lab}-1.py", encoding="utf-8").read()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', txt, re.S)
    expected = html.unescape(e.group(1))
    got = open(f"{out_dir}/twin_lab-CS2-{lab}-1.out", encoding="utf-8").read()
    print(lab, "page code == twin (rstrip):", code.rstrip() == twin.rstrip(), "| len", len(code), len(twin),
          "| expected == twin output:", expected.rstrip("\n") == got.rstrip("\n"),
          "| twin ends with main():", twin.rstrip().endswith("main()"))
    if code.rstrip() != twin.rstrip():
        import difflib
        for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0):
            print("   ", l)
    if expected.rstrip("\n") != got.rstrip("\n"):
        import difflib
        for l in difflib.unified_diff(got.splitlines(), expected.splitlines(), lineterm="", n=0):
            print("   ", l)
    # twin must not use the __name__ guard
    print("   has __main__ guard:", "__main__" in twin, "| has data-files:", "data-files" in txt)
