"""Locate each quotation of a claim span (with a gpo key) on the printed page of the opinion it cites.

usage: python3 -I loccheck_r10.py <page.html> <scratch_dir_with_pdfs_and_quotecheck>
Reads the two USREPORTS PDFs in the scratch dir with pdftotext, one page at a time (pdf page i = printed page i + offset).
Prints OK when a quotation's first 5-word piece occurs on a page inside the claim's locator set, CHK otherwise.
"""
import html
import re
import subprocess
import sys

scratch = sys.argv[2]
sys.path.insert(0, scratch)
from quotecheck_r10 import norm  # noqa: E402


def pages(pdf: str, offset: int) -> dict[int, str]:
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    out: dict[int, str] = {}
    for i in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"], capture_output=True, text=True).stdout
        t = t.replace("-\n", "").replace("\n", " ")
        t = norm(t).replace("*", " ")
        out[i + offset] = re.sub(r"\s+", " ", t)
    return out


SRC = {
    "gpo1983dirks": pages(f"{scratch}/USREPORTS-463-646.pdf", 645),
    "gpo1997united": pages(f"{scratch}/USREPORTS-521-642.pdf", 641),
}


def locset(loc: str) -> set[int]:
    s: set[int] = set()
    for a, b in re.findall(r"pp?\. (\d{3})(?:[-–](\d{3}))?", loc):
        s.add(int(a))
        if b:
            s.update(range(int(a), int(b) + 1))
    for chunk in re.findall(r"(?:,|and) (\d{3})\b", loc):
        s.add(int(chunk))
    return s


def main() -> None:
    text = open(sys.argv[1], encoding="utf-8").read()
    for m in re.finditer(r'<span class="claim"[^>]*data-grade="[^"]*" data-cite="([^"]*)" data-locator="([^"]*)"[^>]*>(.*?)</span>', text, re.S):
        cites, loc, body = m.group(1).split(), html.unescape(m.group(2)), re.sub(r"<[^>]+>", "", m.group(3))
        quotes = re.findall(r"“([^”]{15,})”", body)
        cited = [c for c in cites if c in SRC]
        if not quotes or not cited:
            continue
        L = locset(loc)
        if not L:
            print("NOLOC", loc, "|", body[:60])
            continue
        for q in quotes:
            qn = norm(q).strip(" .,;:")
            pieces = [p.strip(" .,;:") for p in re.split(r"\[[^\]]*\]|\.\.\.|…", qn) if len(p.split()) >= 5]
            if not pieces:
                continue
            found: set[int] = set()
            for c in cited:
                for pg, tx in SRC[c].items():
                    norm_tx = tx.replace("‘", "'").replace("’", "'").lower()
                    if all(p.replace("‘", "'").replace("’", "'").lower() in norm_tx for p in pieces):
                        found.add(pg)
            ok = bool(found & L)
            print("OK " if ok else "CHK", cited, loc, "found_pages=", sorted(found), "|", qn[:70])


if __name__ == "__main__":
    main()
