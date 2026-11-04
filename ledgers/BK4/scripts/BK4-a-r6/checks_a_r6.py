"""Round-6 BK4 slice a text and notation checks over index, L01, L02, L03 (raw HTML, stdlib only).
Usage: python3 -I checks_a_r6.py <checkout root>. Prints every check with its observed result."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/BK/BK4"
pages = ["index", "L01", "L02", "L03"]


def visible(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", " ", t)))


def math_spans(path: Path) -> list[str]:
    t = path.read_text(encoding="utf-8")
    return [m.group(1) or m.group(2) or "" for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)]


# 1. notation: registered symbols/macros (notation/notation.json) must not appear with another meaning
registered = [r"\\mathbb\{R\}", r"\\R\b", r"\\Phi", r"\\gamma", r"\\Var", r"\\E\b", r"\\Cov", r"\\Corr", r"\\Prob",
              r"\\mathbb\{Q\}", r"R\^\\ast", r"R\^\{e\\ast\}", r"R_f", r"\bT\b", r"\\SR", r"\\N\b", r"\\emgamma"]
spans_all = []
for p in pages:
    spans = math_spans(base / f"{p}.html")
    spans_all += [(p, s) for s in spans]
    print(f"[notation] {p}: {len(spans)} math spans")
macros = sorted(set(re.findall(r"\\([A-Za-z]+)", " ".join(s for _, s in spans_all))))
print("[notation] macros used:", macros)
for pat in registered:
    hits = [(p, s[:70]) for p, s in spans_all if re.search(pat, s)]
    print(f"[notation] registered pattern {pat!r}: {len(hits)} hits", hits[:2])

# 2. banned phrases and process words in visible text
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "builder", "verifier", "fixer", "planner", "precedent", "architect", "REQUEST",
          "ledger", "unit report", "round "]
for p in pages:
    vis = visible(base / f"{p}.html")
    found = {b: len(re.findall(re.escape(b), vis, re.I)) for b in banned}
    found = {b: n for b, n in found.items() if n}
    print(f"[words] {p}: banned/process hits {found}")
    print(f"[words] {p}: ellipsis char count {vis.count(chr(0x2026))} three-dot count {vis.count('...')}")

# 3. why-it-matters length (BUILDER_RULES: at most 120 words)
for p in ["L01", "L02", "L03"]:
    t = (base / f"{p}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    print(f"[why] {p}: {len(visible_text) if False else len(html.unescape(re.sub(r'</?[a-zA-Z][^>]*>', '', m.group(1))).split())} words")

# 4. DAG: out-of-closure concept names (plan section 4, D1-D13) in visible text of the slice
names = ["futures", "variation margin", "haircut", "bank reserves", "central bank", "central-bank",
         "value-at-risk", "value at risk", "expected shortfall", "stress test", "monte carlo", "variance",
         "covariance", "liquidity coverage", "net stable", "safe asset", "recovery waterfall", "credit default",
         "central clearing mandate", "treasury", "model risk", "present value", "geometric series", "Bertrand",
         "bank money creation", "bank run", "run on repo", "liquidity spiral", "procyclical"]
for p in pages:
    vis = visible(base / f"{p}.html").lower()
    print(f"[dag] {p}:", {n: vis.count(n.lower()) for n in names if vis.count(n.lower())})

# 5. data citations and grades
for p in pages:
    t = (base / f"{p}.html").read_text(encoding="utf-8")
    print(f"[cite] {p}: data-cite keys", re.findall(r'data-cite="([^"]+)"', t))
    print(f"[grade] {p}: grade blocks", sorted(set(re.findall(r'data-grade="([^"]+)"', t))))

# 6. hub claim scope: out-of-slice pages must not use the concepts the hub says no lesson uses
for p in ["L04", "L05"]:
    vis = visible(base / f"{p}.html").lower()
    print(f"[hub-claim] {p}: present value {vis.count('present value')}, geometric {vis.count('geometric')}, "
          f"bertrand {vis.count('bertrand')}, limit-as-word {len(re.findall(r'[^ ]+ limit|limit of', vis))}")
vis = visible(base / "project.html").lower()
print(f"[hub-claim] project: present value {vis.count('present value')}, geometric {vis.count('geometric')}, "
      f"bertrand {vis.count('bertrand')}")
