"""SC1-a round 16: prerequisite closure and the owner of every concept linked in the hub's prerequisite list."""

import re
import sys

sys.path.insert(0, "tools")
import coursekit as ck  # noqa: E402

print("closure", sorted(ck.prerequisite_closure("SC1")))
owners = ck.concept_owner()
sc1 = sorted(k for k, v in owners.items() if v == "SC1")
print("SC1-owned concepts", len(sc1), sc1)
s = open("course/modules/SC/SC1/index.html", encoding="utf-8").read()
hub = s[s.index('id="prerequisites"'):s.index('id="placement"')]
for g, body in re.findall(r"<li>From (\S+): (.*?)</li>", hub, re.S):
    ids = re.findall(r'data-concept="([^"]+)"', body)
    print(g, [(i, owners.get(i)) for i in ids])
