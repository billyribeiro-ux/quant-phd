# For index and L01-L04: every plain-text chunk (>= 5 words, between math spans and real tags) of the page source must
# occur, as a contiguous run of letter-tokens, in the Chromium-rendered text of <main>. A raw "<" that is not a real tag is
# escaped first (so a bogus tag does not hide source text from the source side). Run from the checkout root.
import html, re
from playwright.sync_api import sync_playwright
P = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a/course/modules/M/M5/"
pages = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]
TAGS = r"(a|abbr|b|blockquote|body|br|button|caption|code|col|dd|details|div|dfn|dl|dt|em|fieldset|figcaption|figure|footer|h[1-6]|head|header|html|i|input|label|legend|li|link|main|meta|nav|ol|option|p|pre|script|section|small|span|strong|style|sub|summary|sup|svg|table|tbody|td|template|textarea|th|thead|title|tr|u|ul|var|path|circle|line|rect|g|text|tspan|desc|title)"
def toks(s):
    return re.findall(r"[A-Za-z]+", s)
def chunks(raw):
    body = raw[raw.find("<main"):raw.find("</main>")]
    body = re.sub(r"<(script|style|pre)\b.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<(?!/?" + TAGS + r"[\s>/])", "&lt;", body, flags=re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"\\\((.*?)\\\)", " MATHX ", body, flags=re.S)
    body = re.sub(r"\\\[(.*?)\\\]", " MATHX ", body, flags=re.S)
    out = []
    for part in body.split("MATHX"):
        t = toks(part)
        if len(t) >= 5:
            out.append(t)
    return out
def contains(hay, needle):
    n = len(needle)
    first = needle[0]
    for i, tok in enumerate(hay):
        if tok == first and hay[i:i+n] == needle:
            return True
    return False
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page()
    for name in pages:
        raw = open(P + name, encoding="utf-8").read()
        p.goto("file://" + P + name)
        p.wait_for_timeout(600)
        rendered = toks(p.evaluate("() => document.querySelector('main').innerText"))
        misses = []
        cs = chunks(raw)
        for c in cs:
            if not contains(rendered, c):
                misses.append(" ".join(c)[:150])
        print(f"{name}: chunks {len(cs)}, misses {len(misses)}")
        for m in misses:
            print("   MISS:", m)
    b.close()
