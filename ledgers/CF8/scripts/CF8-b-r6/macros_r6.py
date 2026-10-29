"""List every LaTeX control word used in the L03-L05 pages and the twins, and flag any not in the KaTeX core set or registry macros."""
import json, re, sys
ROOT = sys.argv[1]
reg = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))["macros"]
reg_names = {m.lstrip("\\") for m in reg}
core = {"ldots","lceil","rceil","lfloor","rfloor","frac","sqrt","sum","max","min","mathrm","text","quad","bigl","bigr","Bigl","Bigr","le","ge","lt","gt","ast","cdots","operatorname","left","right","bar","mathbb","bigl","mathcal","cdot","times","sim","approx","in","subseteq","lVert","mid","dfrac","tfrac","mathbf","emph","ell","exp","log","prod","pm","neq","to","infty","alpha","beta","sigma","mu","gamma","delta","Delta","theta","eta","lambda","rho","pi","epsilon","nu","sum","hat","bar","overline","underline","vert","lbrace","rbrace","qquad","mathit","operatorname","mathsf","mathrm","ldots","lt","gt","quad","displaystyle","eqref"}
for f in ["course/modules/CF/CF8/L03.html","course/modules/CF/CF8/L04.html","course/modules/CF/CF8/L05.html","tests/labs/CF8/lab-CF8-L03-1.py","tests/labs/CF8/lab-CF8-L04-1.py","tests/labs/CF8/lab-CF8-L05-1.py"]:
    text = open(f"{ROOT}/{f}", encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    words = set()
    for a, b in maths:
        words |= set(re.findall(r"\\([A-Za-z]+)", a + b))
    odd = sorted(w for w in words if w not in core and w not in reg_names)
    print(f, "control words:", sorted(words))
    print(f, "not in core or registry:", odd)
