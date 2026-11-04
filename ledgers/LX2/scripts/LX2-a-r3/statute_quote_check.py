"""Find every curly-quoted passage in a lesson page that sits in a statute claim span, in the GovInfo compilation text.

Usage: python3 -I statute_quote_check.py <page.html> <comps1884.txt> <comps1885.txt>
Matching uses lowercase letters and digits only on both sides (quote variants, dashes, line breaks and punctuation are
dropped). A passage is looked up in the compilation of its span's cite key (gpondsecurities -> 1884, gpondsecuritiesb
-> 1885). Prints FOUND or NOT-FOUND per passage, then the total.
"""

import html
import re
import sys


def alnum(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main() -> None:
    page = open(sys.argv[1], encoding="utf-8").read()
    texts = {
        "gpondsecurities": alnum(open(sys.argv[2], encoding="utf-8", errors="replace").read()),
        "gpondsecuritiesb": alnum(open(sys.argv[3], encoding="utf-8", errors="replace").read()),
    }
    spans = re.findall(r'<span class="claim"([^>]*)>(.*?)</span>', page, flags=re.S)
    total = found = 0
    for attrs, body in spans:
        cite = re.search(r'data-cite="([^"]*)"', attrs).group(1).split()
        loc = re.search(r'data-locator="([^"]*)"', attrs).group(1)
        if not any(c in texts for c in cite):
            continue
        plain = html.unescape(re.sub(r"<[^>]+>", "", body))
        for q in re.findall(r"“(.*?)”", plain, flags=re.S):
            key = alnum(q)
            if len(key) < 12:
                continue
            total += 1
            hit = [c for c in cite if c in texts and key in texts[c]]
            if hit:
                found += 1
                print(f"FOUND     [{hit[0]}] {loc} :: {q[:70]!r}")
            else:
                print(f"NOT-FOUND [{','.join(cite)}] {loc} :: {q[:110]!r}")
    print(f"statute quotations in claim spans: {total}, found {found}, not found {total - found}")


main()
