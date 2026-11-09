# Scan of course/modules/FC/FC1/cards.json at HEAD against the base pin 95f3f8cb.
import json, re, sys
CK = "/Users/billyribeiro/.fanout/wt/verifyG1-FC1-b"
OUT = CK + "/ledgers/FC1/scripts/FC1-b-r1/out"
head = json.load(open(CK + "/course/modules/FC/FC1/cards.json", encoding="utf-8"))
base = json.load(open(OUT + "/cards_base_95f3.json", encoding="utf-8"))
print("entries head", len(head), "base", len(base))
ids = [c["id"] for c in head]
print("unique ids", len(set(ids)) == len(ids), "same id set", set(ids) == {c["id"] for c in base})
bm = {c["id"]: c for c in base}
print("changed entries", sorted(c["id"] for c in head if bm[c["id"]] != c))
print("order identical", [c["id"] for c in base] == ids)
print("lessons", sorted({c["lesson"] for c in head}))
print("keys", sorted({tuple(sorted(c)) for c in head}))
fr = [c["front"].strip().lower() for c in head]
bk = [c["back"].strip().lower() for c in head]
print("duplicate fronts", len(fr) - len(set(fr)), "duplicate backs", len(bk) - len(set(bk)))
src = open(CK + "/tools/check_pages.py", encoding="utf-8").read()
pats = re.findall(r'r"([^"]+)"', re.search(r"BANNED = \((.*?)\n\)", src, re.S).group(1))
hits = [(c["id"], f, p) for c in head for f in ("front", "back") for p in pats if re.search(p, c[f], re.I)]
print("banned patterns", len(pats), "hits", hits)
pw = re.compile(r"\b(round|verifier|builder|slice|delta|pin|ruling|fanout|checkout|closing|rubric)\b", re.I)
print("process-word hits", [(c["id"], f, pw.search(c[f]).group(0)) for c in head for f in ("front", "back") if pw.search(c[f])])
fx = re.compile(r"Fixture [AB]")
print("lab-name 'Fixture' hits (not process words)", [(c["id"], f) for c in head for f in ("front", "back") if fx.search(c[f])])
print("grades", {g: sum(1 for c in head if c.get("grade") == g) for g in ("T", "C", "X")})
print("absent", {i: (i in ids) for i in ("FC1-c125", "FC1-c173", "FC1-c174")})
