"""Round-13 check: every fragment and file link in course/modules/E/E4/project.html resolves (run from the checkout root)."""
import html.parser, os, re, sys
PAGE = "course/modules/E/E4/project.html"
base = os.path.dirname(PAGE)
src = open(PAGE, encoding="utf-8").read()
ids = set(re.findall(r'\sid="([^"]+)"', src))
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.links.append(v)
p = P(); p.feed(src)
bad = []
for href in p.links:
    if href.startswith(("http://", "https://", "mailto:")):
        bad.append(("external", href)); continue
    if href.startswith("#"):
        if href[1:] not in ids: bad.append(("missing anchor", href))
        continue
    path, _, frag = href.partition("#")
    target = os.path.normpath(os.path.join(base, path))
    if not os.path.exists(target):
        bad.append(("missing file", href, target)); continue
    if frag and target.endswith(".html"):
        other = open(target, encoding="utf-8").read()
        if frag not in set(re.findall(r'\sid="([^"]+)"', other)):
            bad.append(("missing target anchor", href))
print(f"links checked: {len(p.links)}; problems: {bad}")
