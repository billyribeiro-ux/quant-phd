# Round-3 scan (slice c): macros used in L07-L09 math, raw expansions that have registered macros, process words,
# attribution words, declared hours, and the cross-lesson targets the pages cite. Run from the checkout root.
import collections, json, re, sys
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
M3 = root / "course/modules/M/M3"
pages = ["L07.html", "L08.html", "L09.html"]
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered = {k for k in reg.get("macros", {})}
print("registered macros:", sorted(registered))
for p in pages:
    t = (M3 / p).read_text(encoding="utf-8")
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)
    s = " ".join(a or b for a, b in maths)
    cmds = collections.Counter(re.findall(r"\\[A-Za-z]+", s))
    print(f"== {p} macros: {dict(sorted(cmds.items()))}")
    print(f"   raw \\operatorname{{tr}}/{{diag}}: {len(re.findall(r'operatorname\\{(tr|diag)\\}', t))}; \\mathbb uses: {len(re.findall(r'mathbb', t))}; \\operatorname uses: {len(re.findall(r'operatorname', t))}")
    m = re.search(r'data-hours="(\d+)"', t)
    print(f"   data-hours: {m.group(1) if m else None}")
    bad = re.findall(r"TODO|TBD|lorem|for brevity|beyond the scope|details omitted|left as an exercise|it is important to note|well known|obviously|clearly", t, re.I)
    print(f"   banned/process strings: {bad}")
    attr = re.findall(r"Axler|Strang|Higham|Litterman|Scheinkman|Eckart|data-cite|data-locator|et al", t)
    print(f"   attribution tokens: {attr}")
    print(f"   'builder|verifier|architect|round|pin' hits: {len(re.findall(r'builder|verifier|architect|\\bround\\b|\\bpin\\b', t, re.I))}")
hub = (M3 / "index.html").read_text(encoding="utf-8")
hrs = {p: int(re.search(r'data-hours="(\d+)"', (M3 / f"L0{i}.html").read_text(encoding="utf-8")).group(1)) for i, p in enumerate([f"L0{i}" for i in range(1, 10)], 1)}
print("lesson hours:", hrs, "sum =", sum(hrs.values()))
print("hub:", re.findall(r'data-hours-[a-z]+="\d+"', hub))
# cross-lesson targets read in the earlier lessons
l01 = (M3 / "L01.html").read_text(encoding="utf-8"); l06 = (M3 / "L06.html").read_text(encoding="utf-8"); l05 = (M3 / "L05.html").read_text(encoding="utf-8"); l04 = (M3 / "L04.html").read_text(encoding="utf-8")
print("L01 Theorem 3.7 spanned list statement:", "Theorem 3.7" in l01 and "span" in l01[l01.find("Theorem 3.7"):l01.find("Theorem 3.7")+400])
print("L01 subspace defined (Definition/Proposition 'subspace test'):", "subspace test" in l01)
print("L06 Fact 1.2 (QQ^T = I):", "Fact 1.2" in l06 and "QQ^{\\top} = I" in l06)
print("L06 inner product defined:", "inner product" in l06[:4000])
print("L05 Theorem 2.1 eigenvalue test for PSD:", "eigenvalue test for positive semidefiniteness" in l05)
print("L04 Theorem 2.3 spectral theorem:", "Theorem 2.3" in l04 and "spectral theorem" in l04)
print("L04 F1-F4 listed:", all(f"F{i}" in l04 for i in range(1, 5)))
print("L06 sign freedom remark:", "sign" in l06)
