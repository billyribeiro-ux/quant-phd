# For index, L01-L04: every text block of the source (p, li, dd, dt, td, th, caption, summary, h2-h4) must appear, with
# letters and digits only, inside the rendered Chromium textContent of some element. KaTeX keeps the TeX source in its
# MathML annotation, so math is compared too. Raw "<" that is not a real tag is escaped first. Run from the checkout root.
import html, re
from playwright.sync_api import sync_playwright
P = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a/course/modules/M/M5/"
pages = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]
TAGS = r"(a|abbr|b|blockquote|body|br|button|caption|code|col|dd|details|div|dfn|dl|dt|em|fieldset|figcaption|figure|footer|h[1-6]|head|header|html|i|input|label|legend|li|link|main|meta|nav|ol|option|p|pre|script|section|small|span|strong|style|sub|summary|sup|svg|table|tbody|td|template|textarea|th|thead|title|tr|u|ul|var|path|circle|line|rect|g|text|tspan|desc)"
def alnum(s):
    return re.sub(r"[^A-Za-z0-9]", "", s)
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page()
    for name in pages:
        raw = open(P + name, encoding="utf-8").read()
        raw = raw[raw.find("<main"):raw.find("</main>")]
        raw = re.sub(r"<(?!/?" + TAGS + r"[\s>/])", "&lt;", raw, flags=re.I)
        blocks = re.findall(r"<(p|li|dd|dt|td|th|caption|summary|h2|h3|h4)\b[^>]*>(.*?)</\1>", raw, re.S | re.I)
        src = []
        for _, inner in blocks:
            t = re.sub(r"<(script|style)\b.*?</\1>", "", inner, flags=re.S | re.I)
            t = re.sub(r"<[^>]+>", "", t)
            a = alnum(html.unescape(t))
            if len(a) >= 12:
                src.append(a)
        p.goto("file://" + P + name); p.wait_for_timeout(600)
        dom = p.evaluate("""() => Array.from(document.querySelectorAll('main p, main li, main dd, main dt, main td, main th, main caption, main summary, main h2, main h3, main h4')).map(e => e.textContent)""")
        domalnum = [alnum(x) for x in dom]
        joined = "\n".join(domalnum)
        miss = [a for a in src if a not in joined]
        print(f"{name}: blocks {len(src)}, missing from rendered text {len(miss)}")
        for m in miss[:20]:
            print("   MISS:", m[:160])
    b.close()
