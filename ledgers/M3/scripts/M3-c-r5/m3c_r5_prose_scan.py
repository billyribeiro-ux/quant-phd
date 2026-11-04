"""Round-5 prose scan (M3-c): banned phrases, process words, scope words, concept words, ellipses, and
why-it-matters word counts over L07, L08, L09. Run: .venv/bin/python -I ledgers/M3/scripts/M3-c-r5/m3c_r5_prose_scan.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M3-c/course/modules/M/M3")
PAGES = ["L07.html", "L08.html", "L09.html"]
GROUPS = {
    "banned-1.3": ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
                   "you can add more", "important to note", "studies show", "experts agree", "well known",
                   "obviously", "clearly", "it can be shown"],
    "process-words": ["builder", "verifier", "architect", "round", "ledger", "open item", "build plan", "planner",
                      "B1", "B2", "B3", "B4", "DAG", "DATA_REQUEST", "REFERENCE_REQUEST", "Haiku", "placeholder",
                      "Q1", "Q2", "Q3", "Q4", "Section 10"],
    "scope-words": [r"\bevery\b", r"\ball\b", r"\balways\b", r"\bany\b", r"\bonly\b", r"\bexactly\b", r"for all",
                    r"\bsame\b", r"\bdrives\b", r"\bnever\b", r"\bgeneric\b", r"\btypically\b", r"\bin practice\b",
                    r"\bstable\b", r"\brobust\b"],
    "concept-words": [r"\bcovariance\b", r"\bcorrelation\b", r"\bvariance\b", r"\bexpectation\b", r"\bCholesky\b",
                      r"IEEE", r"\bweights?\b", r"Higham", r"Litterman", r"Eckart", r"Treasury", r"\bH\.15\b",
                      r"\bFed\b", r"\bsample covariance\b"],
    "ellipsis": ["…", "..."],
}
for page in PAGES:
    raw = (ROOT / page).read_text(encoding="utf-8")
    # visible text: drop script/style and tags, unescape entities, keep line numbers from the raw file
    lines = raw.split("\n")
    print(f"===== {page} ({len(lines)} lines)")
    for group, pats in GROUPS.items():
        for pat in pats:
            rx = re.compile(pat if pat.startswith(("\\", "(")) or pat in ("…",) or " " in pat and pat.islower() else re.escape(pat) if not pat.startswith(r"\b") and not pat.startswith("for all") else pat, re.I if group in ("banned-1.3", "process-words", "scope-words") else 0)
            hits = []
            for i, line in enumerate(lines, 1):
                for m in rx.finditer(line):
                    s = max(0, m.start() - 50)
                    hits.append((i, line[s:m.end() + 40]))
            if hits:
                print(f"[{group}] {pat}: {len(hits)} hit(s)")
                for i, ctx in hits[:12]:
                    print(f"    L{i}: ...{ctx}...")
    # why-it-matters word count (visible text)
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    text = re.sub(r"\\\((.*?)\\\)", r"\1", text)
    words = len(text.split())
    print(f"why-it-matters words (tags stripped, math text kept): {words}")
