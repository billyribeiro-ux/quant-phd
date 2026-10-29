"""Prose and card scans for M4 slice b (L05-L07), run at the checkout's pin.

Run: python -I ledgers/M4/scripts/M4-b-r4/prose_scan_r4.py
Prints: scope-word sentences, banned and process-word hits, first positions of defined terms against their dfn,
terms outside the prerequisite closure, the MGF and kurtosis grep over L08-L10, and the card duplicate scan.
"""

import collections
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
M4 = ROOT / "course/modules/M/M4"


def visible(path: pathlib.Path) -> str:
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S)
    src = re.sub(r"<pre\b.*?</pre>", " ", src, flags=re.S)
    src = re.sub(r"<code\b.*?</code>", " ", src, flags=re.S)
    src = re.sub(r"\\\((.*?)\\\)", " ", src, flags=re.S)
    src = re.sub(r"\\\[(.*?)\\\]", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return re.sub(r"\s+", " ", html.unescape(src))


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.;:!?])\s+", text)


print("== scope words (L05-L07)")
SCOPE = r"only|all|always|every|any|same|drives|offsets|raises|most|heavy|usually|rare|quickly|large|much|often"
for f in ("L05", "L06", "L07"):
    for i, s in enumerate(sentences(visible(M4 / f"{f}.html"))):
        m = re.search(r"\b(" + SCOPE + r")\b", s, re.I)
        if m:
            print(f, i, m.group(1), "|", s[:150])

print("== banned and process words")
BANNED = (
    r"\bround\b|\bbuild\w*|\bverif\w*|\bREQUEST\w*|\.\.\.|…|\bclearly\b|\bobviously\b|roughly half|about 6%"
    r"|historically|it is important to note|studies show|experts agree|it is well known|\bsimply\b|\btrivially\b"
    r"|can be shown"
)
for f in ("L05", "L06", "L07"):
    print(f, [m.group(0) for m in re.finditer(BANNED, visible(M4 / f"{f}.html"), re.I)])

print("== defined terms: first mention vs dfn (raw HTML character positions)")
TERMS = {
    "L05": {"correlation": "correlation", "covariance matrix": "covariance matrix", "multivariate normal": "multivariate normal"},
    "L06": {"normal distribution": "normal distribution", "Student-t": "Student-t"},
    "L07": {"moment-generating function": "moment-generating function", "characteristic function": "characteristic function"},
}
for f, terms in TERMS.items():
    src = (M4 / f"{f}.html").read_text(encoding="utf-8")
    dfns = {m.group(1): m.start() for m in re.finditer(r'<dfn id="def-([^"]+)"', src)}
    for name, pat in terms.items():
        first = re.search(pat, src, re.I)
        print(f, name, "first at", first.start() if first else None, "dfn positions", dfns)

print("== terms outside the closure (visible prose)")
OUT = r"eigen|determinant|inverse|cholesky|singular|orthogonal|projection|spectral|vector space|linear map|PCA|principal"
for f in ("L05", "L06", "L07"):
    print(f, [m.group(0) for m in re.finditer(OUT, visible(M4 / f"{f}.html"), re.I)])

print("== MGF and kurtosis of the Student-t in L08-L10 (visible prose)")
for f in ("L08", "L09", "L10"):
    t = visible(M4 / f"{f}.html")
    print(f, "moment-generating mentions:", len(re.findall("moment-generating", t, re.I)),
          "| Student-t kurtosis or fourth moment:", len(re.findall(r"kurtosis|fourth moment", t, re.I)))

print("== cards.json duplicate and grade scan")
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print("cards", len(cards), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1],
      "dup fronts", [k for k, v in collections.Counter(fronts).items() if v > 1],
      "dup backs", [k for k, v in collections.Counter(backs).items() if v > 1])
print("lessons", dict(collections.Counter(c["lesson"] for c in cards)))
print("non-T without cite or basis", [c["id"] for c in cards if c.get("grade") != "T" and not (c.get("cite") or c.get("basis"))])
print("T-symbol cards (Student-t variable named T)", [c["id"] for c in cards if re.search(r"\bT(_| |\^|\)|\]|,|$)", c["front"] + " " + c["back"])])
