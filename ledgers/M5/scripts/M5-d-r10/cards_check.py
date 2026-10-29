import json,re,html,collections,pathlib
root=pathlib.Path("course/modules/M/M5")
cards=json.load(open(root/"cards.json"))
print("count",len(cards))
ids=collections.Counter(c["id"] for c in cards); print("dup ids",[k for k,v in ids.items() if v>1])
fr=collections.Counter(c["front"].strip().lower() for c in cards); print("dup fronts",[k for k,v in fr.items() if v>1])
bk=collections.Counter(c["back"].strip().lower() for c in cards); print("dup backs",[k for k,v in bk.items() if v>1])
keys=collections.Counter(tuple(sorted(c)) for c in cards); print("key sets",keys)
lessons={}
def text(p): 
    t=p.read_text(); t=re.sub(r"<[^>]+>"," ",t); return html.unescape(t)
for c in cards:
    L=c["lesson"]
    if L not in lessons: lessons[L]=text(root/f"{L}.html")
    nums=re.findall(r"\d+(?:\.\d+)?", c["back"])
    missing=[n for n in nums if n not in lessons[L]]
    if missing: print("NUM-NOT-IN-LESSON",c["id"],L,missing)
    if c.get("grade") and c.get("grade") not in ("T","C","X","S","P","U"): print("grade?",c["id"],c["grade"])
    if c.get("grade")=="C" and not c.get("basis"): print("C without basis",c["id"])
    if c.get("grade") in ("C","T") and c.get("basis") is None: print("grade no basis", c["id"])
print("grades", collections.Counter(c.get("grade") for c in cards))
