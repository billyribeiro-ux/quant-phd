import re, sys
from pathlib import Path
root = Path("/Users/billyribeiro/.fanout/wt/verifyG1-M3-c")
sys.path.insert(0, str(root / "tools"))
import check_pages as cp  # noqa: E402
SCOPE = r"\b(always|only|exactly|every|all|any|same|whenever|guarantee[sd]?|not always|stable|real data|real curve|each)\b"
for p in ["L07", "L08", "L09"]:
    txt = (root / f"course/modules/M/M3/{p}.html").read_text(encoding="utf-8")
    vis = re.sub(r"<script.*?</script>|<style.*?</style>", " ", txt, flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", vis)
    hits = [m.group(0) for m in re.finditer(SCOPE, vis, flags=re.I)]
    from collections import Counter
    print(p, "scope-word counts:", dict(Counter(h.lower() for h in hits)))
    ell = [m.start() for m in re.finditer(r"\.\.\.|…", txt)]
    print(p, "ellipsis occurrences:", len(ell))
    print(p, "data-cite/data-locator:", txt.count("data-cite"), txt.count("data-locator"), "ol data-references:", re.findall(r"<ol data-references[^>]*>.*?</ol>", txt, flags=re.S)[:1] and "present" or "none")
    print(p, "h2 count:", len(re.findall(r"<h2", txt)), "h3 count:", len(re.findall(r"<h3", txt)))
    print(p, "data-hours:", re.findall(r'data-hours="[^"]*"', txt))
