"""Round-6 slice a (verifier re-run): scan visible prose (tags stripped, math kept) of index.html and L01-L06 for banned phrases, process words, rhetorical questions and scope words."""
import html
import re
import sys

root = sys.argv[1]
pages = ["index.html"] + [f"L0{i}.html" for i in range(1, 7)]
banned = [
    r"TODO", r"TBD", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
    r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
    r"obviously", r"clearly", r"it can be shown", r"\bbuilder\b", r"\bBuilder\b", r"\barchitect\b", r"\bverifier\b",
    r"\bledger\b", r"\bruling\b", r"REFERENCE_REQUEST", r"DAG_DEFECT", r"NOTATION_REQUEST", r"\bround \d", r"\bfixed\b",
    r"\bkilled\b", r"\bmutant", r"\bgrader\b", r"\bsibling\b",
]
scope = r"\b(only|all|always|every|any|same|exactly|drives|never|none)\b"
for p in pages:
    raw = open(f"{root}/course/modules/M/M2/{p}", encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    body = re.sub(r"<pre.*?</pre>", " ", body, flags=re.S)  # code and expected output are not prose
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"\s+", " ", text)
    print(f"== {p}: {len(text)} prose chars")
    for pat in banned:
        for m in re.finditer(pat, text):
            s = max(0, m.start() - 70)
            print(f"  BANNED[{pat}]: ...{text[s:m.end() + 70]}...")
    qs = [m for m in re.finditer(r"[^.?!]{0,120}\?", text)]
    for m in qs:
        print(f"  QUESTION: {m.group(0).strip()[:160]}")
    counts = {}
    for m in re.finditer(scope, text, flags=re.I):
        counts[m.group(0).lower()] = counts.get(m.group(0).lower(), 0) + 1
    print(f"  scope words: {dict(sorted(counts.items()))}")
