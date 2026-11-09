import html, json, re, sys, collections
root = "/Users/billyribeiro/.fanout/wt/verifyS8-M2-a"
for n in range(1, 7):
    page = open(f"{root}/course/modules/M/M2/L0{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    twin = open(f"{root}/tests/labs/M2/lab-M2-L0{n}-1.py", encoding="utf-8").read()
    code = html.unescape(m.group(1))
    print(f"L0{n} page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"] for c in cards]
print("cards total", len(cards), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1],
      "dup fronts", [k for k, v in collections.Counter(fronts).items() if v > 1])
print("slice-lesson cards L01-L06:", {l: sum(1 for c in cards if c["lesson"] == l) for l in ["L01","L02","L03","L04","L05","L06"]})
print("slice-lesson total:", sum(1 for c in cards if c["lesson"] in {"L01","L02","L03","L04","L05","L06"}))
print("cards without grade key in L01-L06:", [c["id"] for c in cards if c["lesson"] in {"L01","L02","L03","L04","L05","L06"} and "grade" not in c])
print("c064 back:", next(c["back"] for c in cards if c["id"] == "M2-c064"))
