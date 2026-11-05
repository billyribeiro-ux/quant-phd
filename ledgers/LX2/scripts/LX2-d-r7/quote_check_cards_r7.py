"""LX2-d round 7: every quoted passage in cards.json must occur in a fetched source (whitespace and hyphen-linebreaks ignored)."""
import json
import re
import sys

src_dir = "/tmp/lx2d-r6-src/"
names = ["COMPS-1884.txt", "COMPS-1885.txt", "USREPORTS-463-646.txt", "USREPORTS-521-642.txt", "cfa3a.txt", "cfa6a.txt", "att.txt", "letter.txt"]
raw = "".join(open(src_dir + n, encoding="utf-8", errors="replace").read() for n in names)
corpus_a = re.sub(r"\s+", "", raw).lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
corpus_b = corpus_a.replace("-", "")
cards = json.load(open(sys.argv[1], encoding="utf-8"))
for c in cards:
    for field in ("front", "back"):
        for q in re.findall(r"“([^”]+)”", c[field]):
            k = re.sub(r"\s+", "", q).lower().replace("’", "'")
            k = k.replace("...", "")
            hit = k in corpus_a or k in corpus_b
            # ellipsis-separated pieces are checked individually
            if not hit and "…" in q:
                parts = [re.sub(r"\s+", "", p).lower() for p in q.split("…") if p.strip()]
                hit = all(p in corpus_a or p in corpus_b for p in parts)
                k = " … ".join(parts)
            print(("MATCH " if hit else "NOMATCH ") + c["id"] + " " + field + " : " + q[:110])
