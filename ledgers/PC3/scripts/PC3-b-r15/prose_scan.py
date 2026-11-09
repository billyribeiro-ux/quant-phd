"""Visible-prose scan of L04-L06: banned strings, process words, scope-word sentences, why-it-matters word counts.
Run: python3 -I prose_scan.py <checkout_root>
"""
import html
import re
import sys

root = sys.argv[1]
BANNED = [r"TODO", r"TBD", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
          r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
          r"it is well known", r"obviously", r"clearly"]
PROCESS = [r"\bbuild\w*", r"\bverifier\w*", r"\bREQUESTS?\b", r"\bunit report\b", r"\bround\b", r"\bfixer\w*"]
SCOPE = re.compile(r"\b(only|every|all|always|never|any|same|exactly)\b", re.I)
for p in ("L04", "L05", "L06"):
    raw = open(f"{root}/course/modules/PC/PC3/{p}.html", encoding="utf-8").read()
    s = re.sub(r"<pre\b.*?</pre>", " ", raw, flags=re.S)
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<(/?)(p|li|h2|h3|div|section|tr|td|th|details|summary|ol|ul|span|li)\b[^>]*>", "\n", s)
    text = html.unescape(re.sub(r"<[^>]+>", " ", s))
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.split("\n")]
    body = "\n".join(lines)
    banned_hits = {b: len(re.findall(b, body)) for b in BANNED}
    banned_hits = {k: v for k, v in banned_hits.items() if v}
    process_hits = {b: len(re.findall(b, body, flags=re.I)) for b in PROCESS}
    process_hits = {k: v for k, v in process_hits.items() if v}
    print(f"== {p}: banned hits {banned_hits}; process hits {process_hits}")
    counts = {w: len(re.findall(r"\b" + w + r"\b", body, flags=re.I)) for w in ["only", "every", "all", "always", "never", "any", "same", "exactly"]}
    print(f"   scope-word counts: {counts}")
    for ln in lines:
        if not SCOPE.search(ln):
            continue
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z(“])", ln):
            if SCOPE.search(sent):
                print("   -", sent[:300])
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, flags=re.S)
    if m:
        wim = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
        print(f"   why-it-matters words: {len(wim.split())}")
