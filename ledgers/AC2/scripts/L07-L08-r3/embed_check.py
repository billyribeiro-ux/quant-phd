"""Compare each page's embedded lab code and expected output with the twin file and the twin's stdout.
Usage: python3 -I embed_check.py <checkout> <stdout_dir>"""
import html, os, re, sys
root, outdir = sys.argv[1], sys.argv[2]
ok_all = True
for page, lab in (("L07", "lab-AC2-L07-1"), ("L08", "lab-AC2-L08-1")):
    src = open(os.path.join(root, f"course/modules/AC/AC2/{page}.html"), encoding="utf-8").read()
    twin = open(os.path.join(root, f"tests/labs/AC2/{lab}.py"), encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1))
    out = open(os.path.join(outdir, f"twin-{page}.txt"), encoding="utf-8").read()
    same_code = code.strip() == twin.strip()
    same_exp = exp.strip() == out.strip()
    print(page, "embedded code == twin:", same_code, "| expected == twin stdout:", same_exp)
    if not same_exp:
        import difflib
        print("\n".join(difflib.unified_diff(out.strip().splitlines(), exp.strip().splitlines(), lineterm="")))
    ok_all = ok_all and same_code and same_exp
print("ALL", ok_all)
