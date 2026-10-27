"""Compare every swept figure state (fig_sweep.json) with an independent Python computation."""
import json
import re
import sys
import math
import numpy as np
from scipy import stats

states = json.load(open(sys.argv[1], encoding="utf-8"))
grid = np.linspace(-9, 10, 190001)
pdf = stats.norm.pdf(grid); cdf = stats.norm.cdf(grid)
def exact(n):
    return float(np.trapezoid(grid * n * pdf * cdf ** (n - 1), grid))
bad = []; n_ok = {"max": 0, "power": 0, "fwer": 0}
for s in states:
    if s["chart"] == "max-sharpe-density":
        years = int(s["value"]); T = years * 252; scale = math.sqrt(252 / T)
        exp_txt = [f"{scale * exact(n):.2f}" for n in (10, 100, 1000)]
        tail = f"{1 - stats.norm.cdf(1 / scale) ** 100:.3f}"
        m = re.search(r"expected best Sharpe ([\d.]+) for N = 10, ([\d.]+) for N = 100, ([\d.]+) for N = 1,000; the best of 100 exceeds 1\.0 with probability ([\d.]+)", s["text"] or "")
        if not m: bad.append(("max-parse", years, s["text"])); continue
        got = [m.group(1), m.group(2), m.group(3)]
        ok = got == exp_txt and (f"{float(m.group(4)):.3f}" == tail)
        if not ok: bad.append(("max", years, got, exp_txt, m.group(4), tail))
        else: n_ok["max"] += 1
    elif s["chart"] == "power-family":
        mu = float(s["value"])
        pw = [stats.norm.cdf(mu - stats.norm.ppf(1 - 0.05 / (2 * m))) + stats.norm.cdf(-mu - stats.norm.ppf(1 - 0.05 / (2 * m))) for m in (1, 10, 100, 1000)]
        exp_txt = [f"{p:.3f}" for p in pw]
        d = s["desc"] or ""
        nums = re.findall(r"centred at ([\d.]+)", d)
        got = re.findall(r"([\d.]+) at m = (?:1|10|100|1,000|1000)\b", d)
        mm = re.search(r"Power is ([\d.]+) at m = 1, ([\d.]+) at m = 10, ([\d.]+) at m = 100, ([\d.]+) at m = 1,?000", d)
        if not mm: bad.append(("power-parse", mu, d[:200])); continue
        g = list(mm.groups())
        ok = g == exp_txt and (nums and abs(float(nums[0]) - mu) < 1e-9)
        if not ok: bad.append(("power", mu, g, exp_txt, nums))
        else: n_ok["power"] += 1
    elif s["chart"] == "fwer-growth":
        a = float(s["value"])
        if s.get("text") is None and not s.get("desc"):
            bad.append(("fwer-empty", a)); continue
        n_ok["fwer"] += 1
print("states ok:", n_ok, "mismatches:", len(bad))
for b in bad[:20]: print("MISMATCH", b)
print("sample power desc:", [x["desc"][-160:] for x in states if x["chart"] == "power-family"][:1])
print("sample power desc mu=5:", [x["desc"][-130:] for x in states if x["chart"] == "power-family" and x["value"] == 5.0][:1])
print("sample fwer desc alpha=0.01:", [x["desc"][-150:] for x in states if x["chart"] == "fwer-growth" and x["value"] == 0.01][:1])
print("sample fwer text alpha=0.1:", [(x["text"] or "")[:160] for x in states if x["chart"] == "fwer-growth" and x["value"] == 0.1][:1])
