import html, json, re, subprocess, sys, collections
root = sys.argv[1]
for page, twin, out in [
    ("course/modules/CF/CF1/L03.html", "tests/labs/CF1/lab-CF1-L03-1.py", "/tmp/cf1-v/CF1-b-r7/lab-CF1-L03-1.out"),
    ("course/modules/CF/CF1/L04.html", "tests/labs/CF1/lab-CF1-L04-1.py", "/tmp/cf1-v/CF1-b-r7/lab-CF1-L04-1.out"),
]:
    text = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_src = open(f"{root}/{twin}", encoding="utf-8").read()
    strip = lambda s: "\n".join(l.rstrip() for l in s.strip().splitlines())
    print(page, "embedded code == twin (stripped):", strip(code) == strip(twin_src))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1)) if e else None
    printed = open(out, encoding="utf-8").read() if expected is not None else ""
    if expected is not None:
        print(page, "expected block == twin stdout (exact):", strip(expected) == strip(printed))
        if strip(expected) != strip(printed):
            print("DIFF expected:", repr(expected[:300])); print("DIFF printed:", repr(printed[:300]))
# cards
cards = json.load(open(f"{root}/course/modules/CF/CF1/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
fr = collections.Counter(c["front"] for c in cards); bk = collections.Counter(c["back"] for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1], "dup backs", [k for k, v in bk.items() if v > 1])
