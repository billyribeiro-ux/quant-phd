"""Round-8 slice checks for E4 L07 to L09 (verifier E4-c). Run from the repository root with the project venv:

    .venv/bin/python ledgers/E4/scripts/E4-c-r8/slice_checks_r8.py
"""
import collections
import glob
import html
import json
import re

PAGES = ["L07", "L08", "L09"]
ROOT = "course/modules/E/E4"


def prose(path):
    t = open(path, encoding="utf-8").read()
    t2 = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", t2))
    return re.sub(r"\s+", " ", txt), t


print("== banned phrases and process words (prose, code blocks excluded)")
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
PROCESS = ["build", "builder", "round", "verifier", "REQUEST", "unit report", "fixer", "ledger", "planner",
           "architect", "DATA_REQUEST"]
for p in PAGES:
    txt, _ = prose(f"{ROOT}/{p}.html")
    hits = [(b, txt[max(0, m.start() - 40):m.end() + 20]) for b in BANNED for m in re.finditer(re.escape(b), txt)]
    phits = [(b, txt[max(0, m.start() - 40):m.end() + 20]) for b in PROCESS
             for m in re.finditer(r"\b" + re.escape(b) + r"\b", txt, flags=re.I)]
    print(p, "banned hits", len(hits), "process hits", len(phits), hits[:5], phits[:5])

print("== scope words (counts; sentences listed in the round-8 scan output)")
SCOPE = ["every", "only", "always", "never", "any", "same", "exactly", "all", "guarantee", "prove", "proves"]
for p in PAGES:
    txt, _ = prose(f"{ROOT}/{p}.html")
    print(p, {w: len(re.findall(r"\b" + w + r"\b", txt, flags=re.I)) for w in SCOPE})

print("== rounded figures in prose that are not printed digits")
for p in PAGES:
    txt, _ = prose(f"{ROOT}/{p}.html")
    for pat in [r"0\.013\b", r"0\.167\b", r"0\.002708", r"0\.135\b", r"0\.1277\b", r"0\.1733\b"]:
        for m in re.finditer(pat, txt):
            print(p, pat, "::", txt[max(0, m.start() - 80):m.end() + 30])

print("== definition ids (dfn) unique across E4 pages; links resolve")
pages = {p: open(p, encoding="utf-8").read() for p in sorted(glob.glob(f"{ROOT}/*.html"))}
defs = collections.defaultdict(list)
for p, t in pages.items():
    for m in re.finditer(r'<dfn[^>]*id="(def-[^"]+)"', t):
        defs[m.group(1)].append(p.rsplit("/", 1)[1])
print("duplicate def ids:", {k: v for k, v in defs.items() if len(v) > 1})
bad = []
for p, t in pages.items():
    for m in re.finditer(r'href="([^"#]*)#(def-[^"]+)"', t):
        target, anchor = m.group(1), m.group(2)
        if target.startswith("../"):
            continue
        tp = (p.rsplit("/", 1)[0] + "/" + target) if target else p
        if f'id="{anchor}"' not in open(tp, encoding="utf-8").read():
            bad.append((p, target, anchor))
print("broken def links:", bad)

print("== notation: forbidden raw forms in L07 to L09 math")
for p in PAGES:
    _, t = prose(f"{ROOT}/{p}.html")
    print(p, {b: t.count(b) for b in ["\\mathbb", "\\Phi", "\\gamma", "R^\\ast", "\\mathbb{Q}", "\\mathbb{R}", "\\mathbb{E}"]})

print("== cards: duplicates, basis for T cards, cites")
cards = json.load(open(f"{ROOT}/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
fronts = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
backs = collections.Counter(re.sub(r"\W+", " ", c["back"].lower()).strip() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1], "duplicate backs", [k for k, v in backs.items() if v > 1])
print("T cards without basis", [c["id"] for c in cards if c.get("grade") == "T" and not c.get("basis")])
print("L07-L09 cards", sum(1 for c in cards if c["lesson"] in PAGES))

print("== registry record for milgrom1982information (quoted on L09)")
reg = json.load(open("references/references.json", encoding="utf-8"))
rec = [r for r in reg["entries"] if r.get("key") == "milgrom1982information"][0]
print({k: rec[k] for k in ["title", "container", "volume", "issue", "pages", "year", "verified_by"]})
