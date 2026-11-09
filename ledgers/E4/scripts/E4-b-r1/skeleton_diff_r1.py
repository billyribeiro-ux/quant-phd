# Compare the tag/attribute skeleton of L06.html at the base pin and the current pin (text content ignored).
import subprocess, sys
from html.parser import HTMLParser
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b"
class S(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []
    def handle_starttag(self, tag, attrs):
        self.out.append(("<%s %s>" % (tag, sorted(attrs))))
    def handle_endtag(self, tag):
        self.out.append("</%s>" % tag)
def skel(txt):
    s = S(); s.feed(txt); return s.out
for page in ["L06", "L04", "L05"]:
    old = subprocess.run(["git", "-C", ROOT, "show", f"e919577b:course/modules/E/E4/{page}.html"], capture_output=True, text=True).stdout
    new = open(f"{ROOT}/course/modules/E/E4/{page}.html", encoding="utf-8").read()
    a, b = skel(old), skel(new)
    print(page, "tags old", len(a), "new", len(b), "skeleton identical:", a == b)
