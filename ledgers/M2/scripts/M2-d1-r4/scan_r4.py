"""Round-4 scan for banned phrases, registry macros, and scope words on slice d1 (L19-L21, cards). Run with python3 -I."""
import json, re, sys, html
from pathlib import Path
root = Path(sys.argv[1])
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown"]
files = [root / f"course/modules/M/M2/{p}.html" for p in ("L19", "L20", "L21")]
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
texts = {f.name: f.read_text(encoding="utf-8") for f in files}
texts["cards.json (L19-L21 cards)"] = json.dumps([c for c in cards if c["lesson"] in ("L19", "L20", "L21")], ensure_ascii=False)
for name, t in texts.items():
    hits = {b: t.count(b) for b in banned if b.lower() in t.lower()}
    print(name, "banned hits:", hits or "none")
    print(name, "\\mathbb count:", t.count("\\mathbb"), " \\R count:", t.count("\\R"))
for f in files:
    t = f.read_text(encoding="utf-8")
    segs = re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', t, re.S)
    syms = set()
    for a, b in segs:
        s = a or b
        if re.search(r'(?<![A-Za-z\\])T(?![A-Za-z])', s): syms.add("T")
        if re.search(r'(?<![A-Za-z\\])Q(?![A-Za-z])', s): syms.add("Q")
        for m in re.findall(r'R_\{?f\}?|R\^\{?\\ast|R\^\{e', s): syms.add(m)
        if '\\Phi' in s or '\\gamma' in s or '\\E' in s or '\\Prob' in s: syms.add("registered-macro-or-symbol")
    print(f.name, "registry symbols used:", sorted(syms) or "none")
