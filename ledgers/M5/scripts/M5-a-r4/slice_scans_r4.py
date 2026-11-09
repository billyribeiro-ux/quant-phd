# Round-4 scans for M5 slice a (hub + L01-L04 pages, slice cards). Run from the checkout root.
# Prints: banned-phrase hits, ellipses outside <pre>/<code>, registered-notation symbol hits, macro inventory,
# raw "<" followed by a letter in text, and svg count.
import html.parser, json, re, sys
from collections import Counter
P = "course/modules/M/M5/"
pages = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
                    r"it is important to note|studies show|experts agree|it is well known|obviously|clearly|"
                    r"it can be shown|of course|note that|we will|in this section|verifier|builder|round \d|draft|placeholder", re.I)
print("== banned phrase hits (pages)")
for f in pages:
    for i, line in enumerate(open(P + f, encoding="utf-8"), 1):
        for m in banned.finditer(line):
            print(f, i, m.group(0))
cards = json.load(open(P + "cards.json", encoding="utf-8"))
print("== banned phrase hits (cards)")
for c in cards:
    txt = json.dumps(c, ensure_ascii=False)
    for m in banned.finditer(txt):
        print(c["id"], m.group(0))
print("== ellipses outside code/pre (pages)")
class Strip(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.depth = 0; self.out = []; self.raw = []
        self.in_code = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("pre", "code", "script", "style"): self.in_code += 1
        if tag == "svg": self.raw.append("svg")
    def handle_endtag(self, tag):
        if tag in ("pre", "code", "script", "style") and self.in_code: self.in_code -= 1
    def handle_data(self, data):
        if not self.in_code: self.out.append(data)
for f in pages:
    raw = open(P + f, encoding="utf-8").read()
    s = Strip(); s.feed(raw)
    text = "".join(s.out)
    for m in re.finditer(r"\.\.\.|…", text):
        print(f, "ellipsis:", text[max(0, m.start()-40):m.end()+20].replace("\n", " "))
    print(f, "svg count:", raw.count("<svg"), "| data-files:", raw.count("data-files"))
print("== macro inventory (math source in pages)")
mac = Counter()
for f in pages:
    raw = open(P + f, encoding="utf-8").read()
    mac.update(re.findall(r"\\[A-Za-z]+", raw))
print(sorted(mac.items(), key=lambda kv: -kv[1]))
print("== registered symbols in math spans (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q)")
for f in pages:
    raw = open(P + f, encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)", raw, re.S):
        body = m.group(1)
        if re.search(r"\\Phi|\\gamma_[34]|\\ast|R_f|\\mathbb\{Q\}|\\Q\b|(?<![A-Za-z\\])T(?![A-Za-z])", body):
            print(f, m.group(0)[:120])
print("== raw < followed by a letter in page text")
for f in pages:
    for i, line in enumerate(open(P + f, encoding="utf-8"), 1):
        for m in re.finditer(r"<[A-Za-z]", line):
            ctx = line[m.start():m.start()+12]
            if not re.match(r"<(/?)(a|abbr|b|blockquote|body|br|button|caption|code|col|dd|details|div|dfn|dl|dt|em|fieldset|figcaption|figure|footer|h[1-6]|head|header|html|i|input|label|legend|li|link|main|meta|nav|ol|option|p|pre|script|section|small|span|strong|style|sub|summary|sup|svg|table|tbody|td|template|textarea|th|thead|title|tr|u|ul|var)[\s>/]", ctx, re.I):
                print(f, i, ctx)
