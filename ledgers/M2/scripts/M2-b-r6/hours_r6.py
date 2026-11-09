# Round-6 hours arithmetic: data-hours on L07-L12 and the hub split in index.html (fresh read at e896b7a4).
import re
tot = 0
for n in range(1, 25):
    p = f"course/modules/M/M2/L{n:02d}.html"
    t = open(p, encoding="utf-8").read()
    m = re.findall(r'data-hours="([^"]+)"', t)
    if n in range(7, 13):
        print(p, "data-hours:", m)
    tot += float(m[0]) if m else 0
idx = open("course/modules/M/M2/index.html", encoding="utf-8").read()
print("index data-hours-lessons:", re.findall(r'data-hours-lessons="([^"]+)"', idx), "data-hours-project:", re.findall(r'data-hours-project="([^"]+)"', idx))
print("sum of lesson data-hours L01-L24 =", tot)
