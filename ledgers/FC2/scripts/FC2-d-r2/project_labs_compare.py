"""FC2-d r2: page code equals twin, and each expected block equals the twin's output (project.html labs 1-3).
usage: python -I project_labs_compare.py <repo-root> <out-dir>"""
import html, re, subprocess, sys
root, outdir = sys.argv[1], sys.argv[2]
page = open(f"{root}/course/modules/FC/FC2/project.html", encoding="utf-8").read()
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-FC2-project-{n}".*?</section>', page, re.S)
    if sec is None:
        sec = re.search(rf'id="lab-FC2-project-{n}".*?</section>', page, re.S)
    body = sec.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = open(f"{root}/tests/labs/FC2/lab-FC2-project-{n}.py", encoding="utf-8").read()
    print(f"lab {n}: page code == twin: {code.rstrip() == twin.rstrip()} (page {len(code)} chars, twin {len(twin)} chars)")
    out = open(f"{outdir}/lab-FC2-project-{n}.out", encoding="utf-8").read()
    out_lines = [l for l in out.splitlines() if not l.startswith("rc=")]
    print(f"lab {n}: expected block == twin output: {expected.strip() == chr(10).join(out_lines).strip()}")
