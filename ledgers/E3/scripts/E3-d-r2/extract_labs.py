import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
out_dir = sys.argv[2]
import os
os.makedirs(out_dir, exist_ok=True)
# lab sections
for m in re.finditer(r'<section class="lab[^"]*" id="(lab-E3-project-\d)"[^>]*>(.*?)</section>', src, re.S):
    lab_id, body = m.group(1), m.group(2)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code_t = html.unescape(code.group(1)) if code else None
    exp_t = html.unescape(exp.group(1)) if exp else None
    open(os.path.join(out_dir, lab_id + "_page.py"), "w", encoding="utf-8").write(code_t)
    open(os.path.join(out_dir, lab_id + "_expected.txt"), "w", encoding="utf-8").write(exp_t)
    print(lab_id, "code chars", len(code_t), "expected lines", exp_t.count("\n") + 1)
