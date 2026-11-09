# For L01-L04: the page's <pre class="expected"> block (HTML-unescaped) equals the twin's stdout run alone under python -I -W error;
# the page's data-run code block equals the twin file byte for byte. Run from the checkout root after the r4 twin runs.
import html, re, sys
O = "ledgers/M5/scripts/M5-a-r4/"
for k in range(1, 5):
    page = open(f"course/modules/M/M5/L0{k}.html", encoding="utf-8").read()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = html.unescape(exp.group(1)) if exp else None
    code_src = html.unescape(code.group(1)) if code else None
    twin_src = open(f"tests/labs/M5/lab-M5-L0{k}-1.py", encoding="utf-8").read()
    twin_out = open(O + f"r4_twin_L0{k}.out", encoding="utf-8").read()
    err = open(O + f"r4_twin_L0{k}.err", encoding="utf-8").read()
    ex_ok = expected is not None and expected.rstrip("\n") == twin_out.rstrip("\n")
    code_ok = code_src is not None and code_src.rstrip("\n") == twin_src.rstrip("\n")
    print(f"L0{k}: expected==twin_stdout {ex_ok} | page code==twin file {code_ok} | stderr bytes {len(err)} | exit {open(O + f'r4_twin_L0{k}.exit').read().strip()}")
