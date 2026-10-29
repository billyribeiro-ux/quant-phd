"""Compare each L07/L08 page lab <pre><code data-run> with its twin byte for byte, check expected blocks, and probe the twin's functions (no main())."""
import html
import re
import sys

ROOT = sys.argv[1]
pairs = {
    "L07": ("course/modules/FC/FC2/L07.html", "tests/labs/FC2/lab-FC2-L07-1.py"),
    "L08": ("course/modules/FC/FC2/L08.html", "tests/labs/FC2/lab-FC2-L08-1.py"),
}
for name, (page, twin) in pairs.items():
    src = open(f"{ROOT}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    tw = open(f"{ROOT}/{twin}", encoding="utf-8").read()
    print(name, "page code == twin:", code == tw, len(code), len(tw))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    print(name, "expected block present, length", len(html.unescape(exp)))

# probe L08 twin functions without executing main()
tw = open(f"{ROOT}/tests/labs/FC2/lab-FC2-L08-1.py", encoding="utf-8").read()
tw = tw[: tw.rindex("main()")]
ns: dict = {}
exec(compile(tw, "twin_no_main", "exec"), ns)
for price, strike in [(0.50, 120.0), (4.90, 100.0), (99.99999, 100.0), (99.99, 100.0), (0.0, 100.0)]:
    try:
        s, h = ns["implied_volatility"](price, strike)
        print("price", price, "K", strike, "sigma", round(s, 8), "halvings", h)
    except ValueError as e:
        print("price", price, "K", strike, "ValueError:", str(e)[:70])
print("C(K=100,sig=10)", ns["bs_call"](100.0, 100.0, 0.05, 1.0, 10.0))
print("C(K=100,sig=1e-6)", ns["bs_call"](100.0, 100.0, 0.05, 1.0, 1e-6))
