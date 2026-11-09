import html, json, re, subprocess, sys
root = sys.argv[1]
P = root + "/course/modules/M/M3/"
def txt(s):
    s = re.sub(r"<[^>]+>", " ", s); s = html.unescape(s); return re.sub(r"\s+", " ", s)
old = json.loads(subprocess.run(["git", "-C", root, "show", "ccaeeaf4:course/modules/M/M3/cards.json"], capture_output=True, text=True).stdout)
new = json.loads(open(P + "cards.json", encoding="utf-8").read())
oi = {c["id"]: c for c in old}; ni = {c["id"]: c for c in new}
changed = sorted(k for k in oi if k in ni and oi[k] != ni[k])
seg = lambda k: k.startswith("M3-c") and ni.get(k, oi.get(k, {})).get("lesson") in ("L07", "L08", "L09")
print("changed cards L07-L09:", [k for k in changed if seg(k)])
print("changed cards other lessons:", len([k for k in changed if not seg(k)]))
print("removed:", sorted(set(oi) - set(ni)), "added:", sorted(set(ni) - set(oi)))
for k in ("M3-c127", "M3-c145", "M3-c138", "M3-c211"):
    print(k, "byte-identical" if oi.get(k) == ni.get(k) else "changed", "| grade", ni[k].get("grade"), "| basis", ni[k].get("basis"))
L07 = txt(open(P + "L07.html", encoding="utf-8").read())
i = L07.find("Throughout, vectors are columns"); print("L07 notation paragraph:", L07[i:i + 130])
raw6 = open(P + "L06.html", encoding="utf-8").read()
i = raw6.find("Unless a proof says otherwise"); print("L06 notation paragraph:", txt(raw6[i:i + 260]))
L08 = txt(open(P + "L08.html", encoding="utf-8").read())
i = L08.find("Proposition 3.3"); print("L08 misconception 1 present:", "always the level factor" in L08)
L09 = txt(open(P + "L09.html", encoding="utf-8").read())
print("L09 orthogonal cross-ref:", "Orthogonal matrices are as in Lesson 6, Definition 1.1" in L09)
print("L05 PSD dfn lines:", [n + 1 for n, l in enumerate(open(root + "/course/modules/M/M3/L05.html", encoding="utf-8")) if "<dfn" in l and "positive-semidefinite" in l])
