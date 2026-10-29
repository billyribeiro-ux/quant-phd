import html, re, sys
S = sys.argv[1]
for n in range(19, 25):
    page = open(f"course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    twin_out = open(f"{S}/twin_L{n}.out", encoding="utf-8").read()
    if not exp:
        print(f"L{n}: no expected block"); continue
    e = [l.rstrip() for l in html.unescape(exp[0]).strip().splitlines()]
    t = [l.rstrip() for l in twin_out.strip().splitlines()]
    print(f"L{n}: expected lines {len(e)} twin stdout lines {len(t)} equal {e == t}")
    for i, (x, y) in enumerate(zip(e, t)):
        if x != y:
            print("   diff at", i + 1, repr(x)[:150], "|", repr(y)[:150]); break
