"""Round-8 prose scan for E3 slice e (run from the checkout root with the checkout's .venv python -I).

Prints: (1) banned-phrase and process-word hits in visible prose (tags, code, math stripped separately),
(2) exemplar memo word counts (headings included, tags removed, runs of non-space),
(3) every macro used in E3 math spans, checked against notation/notation.json,
(4) the attribution keys and the lessons that carry them (data-cite on claims and the reading lists).
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e")
E3 = ROOT / "course/modules/E/E3"
PAGES = sorted(E3.glob("*.html"))

BANNED = [
    r"\bTODO\b", r"\bTBD\b", r"\blorem\b", r"for brevity", r"details omitted", r"beyond the scope",
    r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
    r"it is well known", r"\bobviously\b", r"\bclearly\b", r"\.\.\.", "…", r"it can be shown",
]
PROCESS = [
    r"\bround\b", r"\brounds\b", r"verifier", r"\bbuilder\b", r"\bBuilder\b", r"\bfixer\b", r"\bledger\b",
    r"\bpin\b", r"\baudit\b", r"\barchitect\b", r"\bfragment\b", r"\bslice\b", r"\bprevious version\b",
    r"\bfixed in\b", r"\bresolved\b", r"\bdeferred\b", r"\bmutant\b", r"\bmutants\b",
]


def visible_text(raw: str) -> str:
    """Visible prose: script, style and code blocks removed, math spans removed, tags stripped, entities decoded."""
    text = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)
    text = re.sub(r"<code class=\"language-python\".*?</code>", " ", text, flags=re.S)
    text = re.sub(r"\\\((.*?)\\\)", " MATH ", text, flags=re.S)
    text = re.sub(r"\\\[(.*?)\\\]", " MATH ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


print("== (1) banned phrases and process words in visible prose")
for page in PAGES:
    vis = visible_text(page.read_text(encoding="utf-8"))
    for pat in BANNED:
        for m in re.finditer(pat, vis, flags=re.I if pat != r"\.\.\." and pat != "…" else 0):
            ctx = vis[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
            print(f"BANNED {page.relative_to(ROOT)} {pat!r}: ...{ctx}...")
    for pat in PROCESS:
        for m in re.finditer(pat, vis):
            ctx = vis[max(0, m.start() - 50): m.end() + 50].replace("\n", " ")
            print(f"PROCESS {page.relative_to(ROOT)} {pat!r}: ...{ctx}...")
print("(end of section 1)")

print("== (2) exemplar memo word counts (project.html)")
raw = (E3 / "project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, raw, flags=re.S)
    block = m.group(0)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, flags=re.S)
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", part)) for part in memos)
    print(ex, "memo blocks:", len(memos), "words:", len(re.findall(r"\S+", text)))
    # Also count with the MathJax-style source as written (math spans count as their characters).
print("(end of section 2)")

print("== (3) macros used in E3 math spans vs notation.json")
notation = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered = set(notation["macros"].keys())
used: dict[str, set[str]] = {}
for page in PAGES:
    src = page.read_text(encoding="utf-8")
    spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, flags=re.S)
    for a, b in spans:
        for cmd in re.findall(r"\\[A-Za-z]+", a + " " + b):
            used.setdefault(cmd, set()).add(page.name)
for cmd in sorted(used):
    tag = "REGISTERED" if cmd in registered else "not-registered"
    print(f"{cmd:16s} {tag:15s} pages: {','.join(sorted(used[cmd]))}")
print("(end of section 3)")

print("== (4) registry keys and the lines that carry them")
for page in PAGES + [E3 / "project.html"]:
    src = page.read_text(encoding="utf-8")
    for m in re.finditer(r'data-cite="([a-z0-9]+)"', src):
        line = src.count("\n", 0, m.start()) + 1
        print(f"{page.relative_to(ROOT)}:{line} data-cite={m.group(1)}")
for key in ("pratt1964risk", "kahneman1979prospect", "epstein1989substitution", "ellsberg1961risk", "gilboa1989maxmin"):
    hits = []
    for page in PAGES:
        for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if key in line:
                hits.append(f"{page.name}:{n}")
    print(key, "->", " ".join(hits))
print("(end of section 4)")
