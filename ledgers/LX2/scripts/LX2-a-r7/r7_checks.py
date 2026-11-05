"""LX2 slice a, round 7: independent re-derivations used as evidence in the fragment ledgers/LX2/LX2-a.json.

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/r7_checks.py <source_dir> <repo_root>
<source_dir> is the fetch_sources.sh output directory (dirks.txt, ohagan.txt, comps1884.txt, comps1885.txt).
Prints: (1) printed pages of key opinion sentences, (2) the hub arithmetic, (3) the L01 lab counts from its
expected block, (4) the L02 lab rows, (5) the statute subsections behind the L01 locators, (6) registry keys and
the absence of the unregistered sources, (7) concept anchors used by the hub and lessons, (8) the printed pages of the
two opinion dissents that the L02 claims omit.
"""

import json
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import quote_locate as q  # noqa: E402  (same directory; loaded with -I from the script's own folder)


def section(title: str) -> None:
    print(f"\n### {title}")


def statute_show(path: str, pattern: str, after: int = 6) -> None:
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            print(f"-- {os.path.basename(path)}:{i + 1} /{pattern}/")
            for j in range(i, min(len(lines), i + after)):
                s = re.sub(r"\s{2,}", " ", lines[j]).strip()
                if s:
                    print(f"   {j + 1}: {s[:130]}")
            return
    print(f"NO MATCH {pattern}")


def main() -> int:
    src, root = sys.argv[1], sys.argv[2]
    dirks = q.load_opinion(os.path.join(src, "dirks.txt"))
    ohagan = q.load_opinion(os.path.join(src, "ohagan.txt"))

    section("1. printed pages of key opinion sentences (running-head page of each form-feed page)")
    checks = [
        ("dirks", dirks, "Scienter in some cases is relevant"),
        ("dirks", dirks, "mere possession of nonpublic"),
        ("dirks", dirks, "Thus, a tippee assumes a fiduciary duty"),
        ("dirks", dirks, "Absent some personal gain"),
        ("dirks", dirks, "reputational benefit that will translate"),
        ("dirks", dirks, "Determining whether an insider personally benefits"),
        ("dirks", dirks, "may not be clear"),
        ("ohagan", ohagan, "does not extend beyond conduct encompassed"),
        ("ohagan", ohagan, "classical theory applies not only to officers"),
        ("ohagan", ohagan, "misappropriation theory holds that a person commits fraud"),
        ("ohagan", ohagan, "Deception through nondisclosure is central"),
        ("ohagan", ohagan, "if the fiduciary discloses to the source"),
        ("ohagan", ohagan, "does not catch all conceivable forms of fraud"),
        ("ohagan", ohagan, "may still be liable under the misappropriation theory"),
        ("ohagan", ohagan, "was not an"),
    ]
    for name, pages, sentence in checks:
        hits = sorted({pg for pg, t in pages if pg and q.alnum(sentence) in t})
        print(f"{name:7s} {sentence[:60]!r}: printed pages {hits}")

    section("1b. dissent starts (printed pages)")
    for name, pages, pat in (
        ("dirks", dirks, "blackmunjdissenting"),
        ("ohagan", ohagan, "opinionofthomasj"),
    ):
        hits = [pg for pg, t in pages if pg and pat in t]
        print(f"{name}: pages mentioning {pat!r}: {hits[:6]}")

    section("2. hub arithmetic (index.html)")
    print("PV 100/1.1 =", round(100 / 1.1, 3), "-> 90.91 to 2 dp")
    print("derivative of x^2 at 3 =", 2 * 3)
    print("partial d/dx (x^2 y) at (2,3) =", 2 * 2 * 3)
    print("quoted spread 100.10-99.50 =", round(100.10 - 99.50, 2))
    print("hit rate 6/8 =", Fraction(6, 8), float(Fraction(6, 8)))
    diffs = [Fraction(f) - Fraction(r) for f, r in ((10, 11), (12, 13), (9, 8))]
    print("bias: differences", [str(d) for d in diffs], "sum", str(sum(diffs)), "mean", str(sum(diffs) / 3), "=",
          round(float(sum(diffs) / 3), 4))
    print("hours 4 x 9 =", 4 * 9, "; 36 + 14 =", 36 + 14, "; project share 14/50 =", Fraction(14, 50), "=", f"{100 * 14 / 50:.0f}%")
    print("lessons share 36/50 =", f"{100 * 36 / 50:.0f}%")
    print("placement: 7 of 10 =", f"{70}% (bar 80%, eight of ten)")

    section("3. L01 lab counts (from the page's expected block)")
    lab = open(os.path.join(root, "course/modules/LX/LX2/L01.html"), encoding="utf-8").read()
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', lab, re.S).group(1)
    states = re.findall(r"^(\w+)\s+(not_listed|listed)\s+yes\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(yes|no)$", expected, re.M)
    print("states listed:", len(states))
    print("sale permitted:", sum(s[5] == "yes" for s in states), "offer permitted:", sum(s[4] == "yes" for s in states),
          "R13 applies:", sum(s[1] == "listed" for s in states), "R15 applies:", sum(s[3] == "yes" for s in states))
    print("transitions printed:", len(re.findall(r"\[section ", expected)))

    section("4. L02 lab rows (from the page's expected block)")
    l02 = open(os.path.join(root, "course/modules/LX/LX2/L02.html"), encoding="utf-8").read()
    exp2 = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', l02, re.S).group(1)
    for line in exp2.split("\n"):
        if re.match(r"^P\d ", line) or line.startswith(("fired:", "not fired:")):
            print(line[:150])

    section("5. statute passages behind the L01 section locators")
    c84 = os.path.join(src, "comps1884.txt")
    c85 = os.path.join(src, "comps1885.txt")
    statute_show(c84, r"If it appears to the Commission that a registration state", 3)
    statute_show(c84, r"^\s*\(e\) The Commission is hereby empowered", 3)
    statute_show(c84, r"\(d\) LIMITATION", 2)
    statute_show(c84, r"EMERGING GROWTH COMPANIES", 3)
    statute_show(c84, r"EXEMPTED SECURITIES 4", 2)
    statute_show(c85, r"shall become effective thirty days", 2)
    statute_show(c85, r"automatically suspended as to any fis", 3)

    section("6. registry keys cited by slice a and the unregistered sources")
    reg = json.load(open(os.path.join(root, "references/references.json"), encoding="utf-8"))
    by = {e["key"]: e for e in reg["entries"]}
    for key in ("gpondsecurities", "gpondsecuritiesb", "gpo1983dirks", "gpo1997united", "cfandcode", "frb2026fed"):
        e = by.get(key)
        print(key, "present" if e else "MISSING", "| year", (e or {}).get("year"), "|", ((e or {}).get("title") or "")[:70])
    text = open(os.path.join(root, "references/references.json"), encoding="utf-8").read().lower()
    print("registry matches for dodd / frank / mifid / texas / gulf / sulphur:",
          [w for w in ("dodd", "mifid", "texas", "gulf", "sulphur") if w in text])

    section("7. concept anchors used by the hub and lessons")
    concepts = open(os.path.join(root, "course/concepts.html"), encoding="utf-8").read()
    for cid in ("exchange-vs-otc", "limit-order-book", "order-types", "bid-ask-spread", "quantifiers", "present-value",
                "derivative", "partial-derivative", "comparative-statics", "evidence-grade", "project-ladder"):
        print(cid, "anchor" if f'id="{cid}"' in concepts else "MISSING")

    print("\nEND")
    return 0


if __name__ == "__main__":
    sys.exit(main())
