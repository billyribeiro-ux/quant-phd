"""Round 17 (BK4 slice c): (1) strip annotations, verdicts and data-score(s) from the exemplar passages of project.html
into a blind copy; (2) compare each project lab's page code block with its twin file under tests/labs/BK4."""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
OUT = ROOT / "ledgers/BK4/scripts/BK4-c-r17/out"
OUT.mkdir(parents=True, exist_ok=True)
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")

# (1) blind exemplar prose: keep only the memo-text div of each article; drop annotation aside, verdict paragraph
blind_parts = []
for art in re.finditer(r'<article class="exemplar" id="(exemplar-[ab])".*?</article>', page, re.S):
    body = art.group(0)
    memo = re.search(r'<div class="memo-text">(.*?)</div>\s*<aside', body, re.S)
    text = re.sub(r"<[^>]+>", " ", memo.group(1))
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    blind_parts.append(f"== {art.group(1)} (annotations, verdict and data-scores removed) ==\n{text}\n")
(OUT / "blind_exemplars_r17.txt").write_text("\n".join(blind_parts), encoding="utf-8")
print("blind exemplar text written:", sum(len(p) for p in blind_parts), "chars")

# (2) page lab code vs twin
for n in (1, 2, 3):
    m = re.search(r'id="lab-BK4-project-%d".*?<pre><code class="language-python" data-run>(.*?)</code></pre>' % n, page, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/BK4/lab-BK4-project-{n}.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(f"lab project-{n}: page code == twin (modulo trailing newline): {same}; page lines {code.count(chr(10))+1}, twin lines {twin.count(chr(10))+1}")
    if not same:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print(line)
