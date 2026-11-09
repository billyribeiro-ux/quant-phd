"""Banned-phrase, process-word, scope-word, macro and cross-reference scan for L09-L11 and the L09-L11 cards (CS2-c r3)."""
import re, sys, collections, json, html
ROOT = sys.argv[1]
pages = [f"{ROOT}/course/modules/CS/CS2/{p}.html" for p in ("L09", "L10", "L11")]
banned = re.compile(r"TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|important to note|studies show|experts agree|well known|obvious|clearly|can be shown|you can add more|details omitted|builder|verifier|architect|round \d|placeholder|draft|planner|\.\.\.|…", re.I)
scope = re.compile(r"\b(every|all|always|never|only|exact|exactly|any|same|drives|stable|optimal|amortized)\b", re.I)
for p in pages:
    s = open(p, encoding="utf-8").read()
    text = html.unescape(re.sub(r"<[^>]+>", " ", s))
    hits = [m.group(0) for m in banned.finditer(text)]
    print(p.split("/")[-1], "banned/process hits:", hits)
    print(p.split("/")[-1], "scope words:", dict(collections.Counter(m.group(0).lower() for m in scope.finditer(text))))
    macros = collections.Counter(re.findall(r"\\[A-Za-z]+", s))
    print(p.split("/")[-1], "macros:", dict(macros))
cards = json.load(open(f"{ROOT}/course/modules/CS/CS2/cards.json", encoding="utf-8"))
bad = [c["id"] for c in cards if re.search(banned, c["front"] + " " + c["back"]) or re.search(r"\.\.\.|…", c["front"] + c["back"])]
print("cards with banned/ellipsis:", bad)
print("cards total", len(cards), "L09-L11", sum(c["lesson"] in ("L09", "L10", "L11") for c in cards))
print("cross-ref check L11 'Section 3, Misconception 2':", "Section 3, Misconception 2" in open(pages[2], encoding="utf-8").read())
print("cross-ref check L11 'Section 3 says what that check':", "Section 3 says what that check" in open(pages[2], encoding="utf-8").read())
print("L09 'All values are the same 2000 values':", "All values are the same 2000 values" in open(pages[0], encoding="utf-8").read())
print("Misconceptions section heading in L11 is s4 (section 4):", bool(re.search(r'<h2 id="s4"><span class="section-number">4</span>Misconceptions', open(pages[2], encoding="utf-8").read())))
