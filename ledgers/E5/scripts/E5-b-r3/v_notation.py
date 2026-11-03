"""List every math segment in L04-L06 that contains a registered symbol or macro, and every bare
single-letter or Greek symbol used, so each can be compared with notation/notation.json by hand."""
import html, json, pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1])
nj = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered = [s.get("symbol", "") for s in nj["symbols"]] + list(nj["macros"].keys())
print("registered:", registered)
for L in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/E/E5/{L}.html").read_text(encoding="utf-8")
    raw = html.unescape(raw)
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S)
    maths = [a or b for a, b in segs]
    hits = {}
    for m in maths:
        for r in registered:
            key = r.split(",")[0].strip()
            if key and key in m:
                hits[key] = hits.get(key, 0) + 1
    print(L, "math segments:", len(maths), "registered-symbol hits:", hits)
    tokens = set()
    for m in maths:
        m2 = re.sub(r"\\(mathrm|text|operatorname|mathbf|bar|tilde|hat|ast|partial|le|ge|neq|frac|left|right|qquad|quad|,|;)", " ", m)
        tokens.update(re.findall(r"\\[A-Za-z]+|[A-Za-z]", m2))
    print(L, "distinct symbol tokens:", sorted(tokens))
