"""List every graded claim title and key-results row grade in L13-L18 (verifier round 3). Standard library only."""
import re
for n in range(13, 19):
    t = open(f"course/modules/M/M2/L{n:02d}.html", encoding="utf-8").read()
    for m in re.finditer(r'<span class="block-title claim" data-grade="([A-Z])">([^<]*)<span class="name">([^<]*)</span>', t):
        print(f"L{n:02d} block {m.group(1)} {m.group(2).strip()} {m.group(3)}")
    rows = re.findall(r'<tr><td>(.*?)</td><td><span class="grade" data-grade="([A-Z])">[A-Z]</span></td><td>(.*?)</td></tr>', t, flags=re.S)
    for r in rows:
        print(f"L{n:02d} key {r[1]} | {re.sub(r'<[^>]+>', '', r[0])[:110]} | src: {re.sub(r'<[^>]+>', '', r[2])[:80]}")
    print(f"L{n:02d} grade-spans-total", len(re.findall(r'data-grade="[A-Z]"', t)))
