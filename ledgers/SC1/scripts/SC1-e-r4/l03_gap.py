import math, re, sys
txt = open(sys.argv[1]).read()
H = None
rows = []
for line in txt.splitlines():
    m = re.match(r"H = (\d+): mean", line)
    if m:
        H = float(m.group(1)); continue
    m = re.match(r"\s+N =\s+(\d+) steps: mean ([\d.]+), se ([\d.]+), z = ([-\d.]+)", line)
    if m and H is not None:
        N = int(m.group(1)); se = float(m.group(3)); z = float(m.group(4)); mean = float(m.group(2))
        pop = H * math.sqrt(2 / N) / 20
        gap = se / pop - 1
        zc = (mean - H) / se
        rows.append((H, N, se, round(pop, 6), round(gap * 100, 2), z, round(zc, 2)))
for r in rows: print(r)
print("max |gap| %", max(abs(r[4]) for r in rows), "max gap", max(r[4] for r in rows), "min gap", min(r[4] for r in rows))
print("max |z|", max(abs(r[5]) for r in rows))
