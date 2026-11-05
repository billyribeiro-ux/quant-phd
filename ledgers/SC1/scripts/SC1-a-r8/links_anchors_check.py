# Round 8: every local href/src in the slice resolves; every #fragment exists in its target; every data-cite key is in the registry.
import html.parser, json, pathlib, sys, re
root = pathlib.Path(sys.argv[1])
pages = [root/"course/modules/SC/SC1"/f"{n}.html" for n in ["index","L01","L02","L03"]]
ids = {}
class P(html.parser.HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path=path; self.hrefs=[]; self.ids=set(); self.cites=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if "id" in d: self.ids.add(d["id"])
        if tag=="a" and "href" in d: self.hrefs.append(d["href"])
        if tag in ("link","script","img") and ("href" in d or "src" in d): self.hrefs.append(d.get("href") or d.get("src"))
        if "data-cite" in d: self.cites.append(d["data-cite"])
parsed={}
for p in pages + [root/"course/concepts.html"]:
    pp=P(p); pp.feed(p.read_text(encoding="utf-8")); parsed[p]=pp
bad=0; n=0
for p in pages:
    for h in parsed[p].hrefs:
        if h.startswith(("http://","https://","mailto:")): print("EXTERNAL", p.name, h); bad+=1; continue
        if h.startswith("#"):
            target=p; frag=h[1:]
        else:
            path, _, frag = h.partition("#")
            target=(p.parent/path).resolve()
        n+=1
        if not target.exists(): print("MISSING FILE", p.name, h); bad+=1; continue
        if frag:
            if target not in parsed:
                tp=P(target); tp.feed(target.read_text(encoding="utf-8")); parsed[target]=tp
            if frag not in parsed[target].ids: print("MISSING ANCHOR", p.name, h); bad+=1
    for c in parsed[p].cites:
        keys = {e["key"] for e in json.load(open(root/"references/references.json",encoding="utf-8"))["entries"]}
        if c not in keys: print("UNKNOWN KEY", p.name, c); bad+=1
print("links checked:", n, "problems:", bad)
