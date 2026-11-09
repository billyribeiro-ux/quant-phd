import re, subprocess, sys
from collections import Counter
root = "/Users/billyribeiro/.fanout/wt/verifyG1-M3-c"
def old(p):
    return subprocess.run(["git", "-C", root, "show", f"95f3f8cb:course/modules/M/M3/{p}.html"], capture_output=True, text=True).stdout
for p in ["L07", "L08", "L09"]:
    new = open(f"{root}/course/modules/M/M3/{p}.html", encoding="utf-8").read()
    o = old(p)
    cs = lambda t: Counter(re.findall(r"\\[A-Za-z]+", t))
    cn, co = cs(new), cs(o)
    print(p, "macros added:", dict(cn - co), "removed:", dict(co - cn))
    print(p, "h2 old/new:", len(re.findall(r"<h2", o)), len(re.findall(r"<h2", new)),
          "h3 old/new:", len(re.findall(r"<h3", o)), len(re.findall(r"<h3", new)),
          "data-grade old/new:", len(re.findall(r"data-grade", o)), len(re.findall(r"data-grade", new)))
    print(p, "ellipsis lines:", [ (i, l.strip()[:90]) for i, l in enumerate(new.split("\n"), 1) if "..." in l or "…" in l])
    print(p, "SIMULATED lines:", [i for i, l in enumerate(new.split("\n"), 1) if "SIMULATED" in l])
