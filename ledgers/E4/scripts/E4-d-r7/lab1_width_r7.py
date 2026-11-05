"""Re-derive the Lab 1 bisection width after each halving (page's step 3 claim) by reading the page's Lab 1 code."""
import re, html, math, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d"
page = open(f"{ROOT}/course/modules/E/E4/project.html", encoding="utf-8").read()
m = re.search(r'id="lab-E4-project-1".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
code = html.unescape(m.group(1))
code = code.replace("main()\n", "")  # run the functions, not the printing main
ns = {}
exec(compile(code, "lab1", "exec"), ns)
low, high = 0.0, 1.0
widths = []
for step in range(1, 61):
    mid = 0.5 * (low + high)
    if ns["gap"](mid) > 0.0:
        low = mid
    else:
        high = mid
    widths.append(high - low)
for k in (1, 2, 3, 4, 52, 53, 54, 55, 59, 60):
    print(f"after halving {k}: width {widths[k-1]:.6e}  2^-{k} = {2.0**-k:.6e}")
print("widths equal from 53 on:", len(set(widths[52:])) == 1, "| 2^-53 =", f"{2.0**-53:.3e}")
print("first k with width == 2^-53:", next(k for k, w in enumerate(widths, 1) if w == 2.0**-53))
print("ulp of 0.5795 =", f"{math.ulp(0.5795):.3e}")
