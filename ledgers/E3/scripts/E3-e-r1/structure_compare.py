"""Compare tag multisets, h1 tags, data-hours and dfn/data-concept ids of index.html and L01-L08.html at two pins."""
import re, subprocess, sys, collections
old, new = sys.argv[1], sys.argv[2]
files = ["index.html"] + [f"L0{i}.html" for i in range(1, 9)]
def show(pin, path):
    return subprocess.run(["git", "show", f"{pin}:course/modules/E/E3/{path}"], capture_output=True, text=True).stdout
for f in files:
    a, b = show(old, f), show(new, f)
    ta = collections.Counter(re.findall(r"<[a-zA-Z0-9]+[ >/]", a))
    tb = collections.Counter(re.findall(r"<[a-zA-Z0-9]+[ >/]", b))
    h1a, h1b = re.findall(r"<h1[^>]*>.*?</h1>", a, re.S), re.findall(r"<h1[^>]*>.*?</h1>", b, re.S)
    hoa, hob = re.findall(r"data-hours[^>]*>", a), re.findall(r"data-hours[^>]*>", b)
    dfa, dfb = re.findall(r'<dfn id="[^"]*" data-concept="[^"]*"', a), re.findall(r'<dfn id="[^"]*" data-concept="[^"]*"', b)
    print(f"{f}: tags_same={ta == tb} h1_same={h1a == h1b} data_hours_same={hoa == hob} dfn_ids_same={dfa == dfb} (dfn {len(dfb)}, h1 {len(h1b)}, data-hours {len(hob)})")
