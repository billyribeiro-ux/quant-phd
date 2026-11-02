import html, re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        a = dict(attrs)
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "section", "div", "pre", "figure", "details", "summary", "dt", "dd", "table", "blockquote"):
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")
        if tag in ("span", "dfn", "a") and a.get("class", "").find("claim") >= 0:
            self.out.append("[" + (a.get("data-grade", "?")) + " cite=" + a.get("data-cite", "") + " loc=" + a.get("data-locator", "") + "]")
        if tag == "a" and "concept" in a.get("class", ""):
            self.out.append("{concept:" + a.get("data-concept", "") + "}")
        if tag == "section" or tag == "pre":
            self.out.append("\n<<" + tag + " " + " ".join(f'{k}="{v}"' for k, v in attrs if k in ("class", "id", "data-runtime", "data-files", "data-packages", "data-tolerance")) + ">>\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "details"):
            self.out.append("\n")
    def handle_data(self, data):
        if self.skip == 0:
            self.out.append(data)

p = P()
p.feed(open(sys.argv[1], encoding="utf-8").read())
t = "".join(p.out)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
sys.stdout.write(t)
