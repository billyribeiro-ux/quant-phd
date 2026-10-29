"""Word count of each lesson's why-it-matters paragraph (BUILDER_RULES 4.2 limit 120); run with python -I."""
import html, re, sys
root = sys.argv[1]
for p in ["L01", "L02"]:
    t = open(f"{root}/course/modules/CF/CF8/{p}.html", encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(p, "why-it-matters words:", len(txt.split()))
