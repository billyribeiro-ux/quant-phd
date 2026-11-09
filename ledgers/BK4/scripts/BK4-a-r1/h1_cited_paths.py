import json
import re
import sys

base = json.load(open("/Users/billyribeiro/.fanout/frags/G-BK4-a.round1.json", encoding="utf-8"))
changed = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
pat = re.compile(r"((?:course|tests|tools|notation|references|curriculum|ledgers|plans|benchmarks|atlas|docs)/[A-Za-z0-9_./\-]*|BLUEPRINT\.md|BUILDER_RULES\.md|VERIFIER_RULES\.md|CLAUDE\.md|README\.md|CURRICULUM\.md)")
cited = {}
for r in base["rows"]:
    for m in pat.findall(r["location"] + " " + r["evidence"]):
        cited.setdefault(m.rstrip(".,;:)"), []).append(r["id"])
hits = []
for p in sorted(cited):
    for c in changed:
        if c == p or c.startswith(p.rstrip("/") + "/") or (p.endswith("/") and c.startswith(p)):
            hits.append((p, c, len(cited[p])))
print("distinct cited paths:", len(cited))
print("cited paths that are changed in 2a805c83..HEAD (path, changed file, rows citing):")
for h in hits:
    print(h)
print("cited paths with no change in range:", sum(1 for p in cited if not any(c == p or c.startswith(p.rstrip('/') + '/') for c in changed)))
