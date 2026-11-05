"""Print each exemplar's memo text only (annotations, official scoring and data-scores removed) for blind scoring."""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, src, re.S)
    body = m.group(0)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', "", body, flags=re.S)
    body = re.sub(r'<aside class="annotation".*?</aside>', "", body, flags=re.S)
    body = re.sub(r"</(h5|p|li|h4)>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n", body).strip()
    print(f"=== {ex} (memo text only) ===")
    print(body)
    print()
