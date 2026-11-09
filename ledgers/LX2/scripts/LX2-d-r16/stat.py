import re, sys
path = sys.argv[1]
flat = re.sub(r"\s+", " ", open(path, encoding="utf-8", errors="replace").read())
for pat in sys.argv[2:]:
    ms = list(re.finditer(pat, flat, flags=re.I))
    print(f"== {pat}: {len(ms)}")
    for m in ms[:2]:
        print("   ...", flat[max(0, m.start()-120): m.end()+330], "...")
