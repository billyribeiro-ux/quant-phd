"""Round-8 static sweeps for M3 slice c (L07, L08, L09, their lab twins and the L07-L09 cards).

Covers: banned phrases (BUILDER_RULES 1.3-1.4), ellipses, why-it-matters word counts, data-hours, math control
sequences against notation.json, external URLs and citation attributes, dfn ids, DAG concept names against
curriculum.json, the delta since the round-7 pin, and the L07-L09 cards (duplicates and a 1-in-10 sample).
Usage: python -I ledgers/M3/scripts/M3-c-r8/static_checks.py <repo_root>
"""

from __future__ import annotations

import collections
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGES = ["L07", "L08", "L09"]
PREV_PIN = "9373ef398589097500ea849e30ff9da423b98943"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def plain(s: str) -> str:
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"\\\((.*?)\\\)", r" \1 ", s, flags=re.S)
    s = re.sub(r"\\\[(.*?)\\\]", r" \1 ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s))


def banned_and_process() -> None:
    print("== banned phrases (BUILDER_RULES 1.3-1.4) and process words")
    phrases = [
        "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
        "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
        "obviously", "clearly", "it can be shown", "verifier", "builder", "ledger", "round ", "previous version",
        "reviewer", "placeholder",
    ]
    for page in PAGES:
        text = plain(read(f"course/modules/M/M3/{page}.html"))
        hits = {p: len(re.findall(re.escape(p), text, flags=re.I)) for p in phrases}
        print(page, {k: v for k, v in hits.items() if v} or "no hits")


def ellipses() -> None:
    print("== ellipsis occurrences (quiz stems followed by options)")
    for page in PAGES:
        raw = read(f"course/modules/M/M3/{page}.html")
        for m in re.finditer(r"…|\.\.\.", raw):
            ctx = plain(raw[max(0, m.start() - 60) : m.end() + 40]).strip()
            print(page, "...", ctx[-90:])


def words_hours() -> None:
    print("== why-it-matters words and data-hours")
    for page in PAGES:
        raw = read(f"course/modules/M/M3/{page}.html")
        wm = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
        assert wm
        hours = re.search(r'data-hours="(\d+)"', raw)
        assert hours
        print(page, "why-it-matters words:", len(plain(wm.group(1)).split()), "data-hours:", hours.group(1))
    total = 0
    for lesson in range(1, 10):
        raw = read(f"course/modules/M/M3/L0{lesson}.html")
        total += int(re.search(r'data-hours="(\d+)"', raw).group(1))  # type: ignore[union-attr]
    hub = read("course/modules/M/M3/index.html")
    print("lesson hours sum:", total, "hub data-hours-lessons:", re.search(r'data-hours-lessons="(\d+)"', hub).group(1))  # type: ignore[union-attr]


def notation() -> None:
    print("== math control sequences vs notation.json macros (non-registered sequences are standard KaTeX)")
    registry = json.loads(read("notation/notation.json"))
    macros = set(registry["macros"].keys())
    standard_local = {"\\top", "\\ast", "\\iota", "\\tau", "\\bar", "\\tilde", "\\hat"}
    for page in PAGES:
        raw = read(f"course/modules/M/M3/{page}.html")
        maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
        text = html.unescape(" ".join(a or b for a, b in maths))
        seqs = collections.Counter(re.findall(r"\\[A-Za-z]+", text))
        registered = sorted(k for k in seqs if k in macros)
        print(page, "registered macros used:", registered)
        print(page, "distinct sequences:", len(seqs), "e.g. local symbols present:", sorted(k for k in seqs if k in standard_local)[:6])
    print("registry symbols:", [s["symbol"] for s in registry["symbols"]])


def citations_urls() -> None:
    print("== citation attributes, external URLs, references blocks, dfn ids")
    for page in PAGES:
        raw = read(f"course/modules/M/M3/{page}.html")
        print(page, "data-cite/data-locator count:", len(re.findall(r"data-cite|data-locator", raw)),
              "external URLs:", len(re.findall(r"https?://", raw)),
              "empty references list:", '<ol data-references></ol>' in raw)
        print(page, "dfn ids:", re.findall(r'<dfn id="([^"]+)"', raw))


def dag_names() -> None:
    print("== DAG concept names: curriculum.json vs the page's introduced concepts")
    cur = json.loads(read("curriculum/curriculum.json"))
    concepts = cur["concepts"]
    for cid in ["orthogonal-projection", "least-squares-projection", "principal-component-analysis",
                "level-slope-curvature", "nearest-correlation-matrix", "eigenvalue-clipping",
                "positive-semidefinite-matrix"]:
        print(cid, "->", repr(concepts.get(cid, {}).get("name")), concepts.get(cid, {}).get("module"))
    for page in PAGES:
        raw = read(f"course/modules/M/M3/{page}.html")
        intro = re.search(r'<strong>Introduces:</strong>(.*?)</li>', raw, re.S)
        print(page, "Introduces row:", plain(intro.group(1)).strip() if intro else None)
    m4 = [k for k, v in concepts.items() if v.get("module") == "M4"]
    for page in PAGES:
        text = plain(read(f"course/modules/M/M3/{page}.html")).lower()
        print(page, "M4 concept name occurrences (covariance|variance|expectation|correlation as a concept):",
              len(re.findall(r"covariance|variance|expectation", text)), "| 'correlation' occurrences:", len(re.findall(r"correlation", text)))
    print("M4 concept ids:", sorted(m4)[:20])


def delta() -> None:
    print("== delta since round-7 pin for slice c paths")
    paths = ["course/modules/M/M3/L07.html", "course/modules/M/M3/L08.html", "course/modules/M/M3/L09.html",
             "course/modules/M/M3/cards.json", "tests/labs/M3", "notation/notation.json", "tools", "curriculum"]
    out = subprocess.run(["git", "-C", str(ROOT), "diff", "--stat", PREV_PIN, "HEAD", "--", *paths],
                         capture_output=True, text=True, check=True).stdout
    print(out.strip())
    twins = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", PREV_PIN, "HEAD", "--", "tests/labs/M3"],
                           capture_output=True, text=True, check=True).stdout.strip()
    print("lab twins changed since round-7 pin:", twins or "none")


def cards() -> None:
    print("== cards L07-L09")
    all_cards = json.loads(read("course/modules/M/M3/cards.json"))
    ids = collections.Counter(c["id"] for c in all_cards)
    fronts = collections.Counter(c["front"] for c in all_cards)
    print("total cards:", len(all_cards), "duplicate ids:", [k for k, v in ids.items() if v > 1],
          "duplicate fronts:", [k for k, v in fronts.items() if v > 1])
    mine = [c for c in all_cards if c["lesson"] in ("L07", "L08", "L09")]
    print("L07-L09 cards:", len(mine))
    for i, c in enumerate(mine):
        if i % 10 == 0:
            print("sample", c["id"], c["lesson"], "grade", c.get("grade"), "|", c["front"], "=>", c["back"][:160])


def main() -> None:
    banned_and_process()
    ellipses()
    words_hours()
    notation()
    citations_urls()
    dag_names()
    delta()
    cards()


if __name__ == "__main__":
    main()
