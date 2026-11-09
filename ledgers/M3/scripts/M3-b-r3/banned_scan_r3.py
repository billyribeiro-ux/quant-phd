"""Round-3 slice b: banned phrases (BUILDER_RULES 1.3-1.4), process words, and scope words in L04-L06 and cards.

Prints each hit with its line. Run from the checkout root.
"""
import re
from pathlib import Path

FILES = [Path(f"course/modules/M/M3/L0{i}.html") for i in (4, 5, 6)] + [Path("course/modules/M/M3/cards.json")]
FILES += [Path(f"tests/labs/M3/lab-M3-L0{i}-1.py") for i in (4, 5, 6)]
BANNED = [r"TODO", r"TBD", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
          r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
          r"obviously", r"clearly", r"it can be shown", r"for every\b.*\bmatrix", r"\bround\b", r"verifier", r"builder",
          r"architect", r"ledger", r"\bagent\b", r"planner", r"\bB[1-4]\b", r"DATA_REQUEST", r"REFERENCE_REQUEST",
          r"previous round", r"fixed in", r"…", r"\.\.\."]
for f in FILES:
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        for p in BANNED:
            for m in re.finditer(p, line, re.I):
                s = max(0, m.start() - 50)
                print(f"BANNED {p!r} {f}:{n}: {line[s:m.end() + 50]!r}"[:260])
print("scan complete")

# Scope words (VERIFIER_RULES 2.x, scope rule): counts in the slice pages and the slice cards only.
import json
SCOPE = r"\b(always|in practice|generic|robust|stable|typically|almost always|for every|every|all|any|only|exactly)\b"
cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards:", len(slice_cards))
for word in ("always", "in practice", "generic", "robust", "stable", "typically"):
    n_pages = sum(len(re.findall(r"\b" + word + r"\b", Path(f"course/modules/M/M3/L0{i}.html").read_text(encoding="utf-8"), re.I)) for i in (4, 5, 6))
    n_cards = sum(len(re.findall(r"\b" + word + r"\b", c["front"] + " " + c["back"], re.I)) for c in slice_cards)
    print(f"scope word {word!r}: slice pages {n_pages}, slice cards {n_cards}")
for i in (4, 5, 6):
    t = Path(f"course/modules/M/M3/L0{i}.html").read_text(encoding="utf-8")
    txt = re.sub(r"<[^>]+>", " ", t)
    print(f"L0{i} scope-word counts:", {w: len(re.findall(r"\b" + w + r"\b", txt, re.I)) for w in ("every", "for every", "all", "any", "only", "exactly")})
print("slice cards scope-word counts:", {w: sum(len(re.findall(r"\b" + w + r"\b", c["front"] + " " + c["back"], re.I)) for c in slice_cards) for w in ("every", "all", "any", "only", "exactly")})
