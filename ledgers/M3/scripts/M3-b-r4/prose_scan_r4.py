"""Round 4 prose scan for the L04-L06 pages and their cards: banned phrases, process words, external
references, figures, citations, notation macros, Cholesky/IEEE, scope words (counts), quiz and why-it-matters counts."""
import html
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
base = root + "/course/modules/M/M3/"
pages = ["L04", "L05", "L06"]
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "motivational", "In this lesson"]
process = [r"\bround\b", r"\bverif\w*", r"\bbuilder\w*", r"\bledger\w*", r"\bslice\b", r"\barchitect\w*", r"\bfixer\w*",
           r"\bpending\b"]
scope = ["always", "every", "all ", "only", "exactly", "any ", "same", "never", "typically", "in practice",
         "generic", "robust", "stable", "whenever"]
for p in pages:
    raw = open(base + p + ".html", encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", body))
    prose = re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", " MATH ", visible, flags=re.S)
    print(f"== {p}")
    print("  http:", raw.count("http"), " data-cite:", raw.count("data-cite"), " svg:", raw.count("<svg"),
          " data-chart:", raw.count("data-chart"), " data-files:", raw.count("data-files"))
    for b in banned:
        n = len(re.findall(re.escape(b), visible, flags=re.I))
        if n:
            print("  banned hit:", repr(b), n)
    for w in process:
        n = len(re.findall(w, prose, flags=re.I))
        if n:
            print("  process-word hit:", w, n)
    for ell in ["…", "..."]:
        hits = [m.start() for m in re.finditer(re.escape(ell), prose)]
        print("  ellipsis", repr(ell), "outside math:", len(hits))
    for w in ["Cholesky", "IEEE", "754", "Higham", "Litterman", "Eckart", "covariance", "correlation", "variance"]:
        n = len(re.findall(w, visible, flags=re.I))
        print("  term", w, n)
    macros = Counter()
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S):
        macros.update(re.findall(r"\\([A-Za-z]+)", m.group(1) or m.group(2)))
    print("  macros:", dict(sorted(macros.items())))
    for w in scope:
        print("  scope", repr(w), len(re.findall(re.escape(w), prose, flags=re.I)))
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, flags=re.S)
    wtxt = re.sub(r"\\\((.*?)\\\)", r"\1", html.unescape(re.sub(r"<[^>]+>", "", why.group(1))))
    print("  why-it-matters words:", len(wtxt.split()))
    print("  items:", raw.count('class="item"'), "explain:", raw.count('class="explain" hidden'),
          "data-correct:", raw.count("data-correct"), "numeric:", raw.count('data-kind="numeric"'))
cards = json.load(open(base + "cards.json", encoding="utf-8"))
bad = [c["id"] for c in cards if re.search(r"TODO|TBD|lorem|process|verifier|builder", c["front"] + c["back"], re.I)]
print("== cards: banned/process hits", bad)
print("== cards with '...' or unicode ellipsis:", [c["id"] for c in cards if "…" in c["front"] + c["back"] or "..." in c["front"] + c["back"]])
