"""LX2-d round 6: locate phrases in an opinion text and report the printed page from the nearest running head.

Usage: python3 -I locate_r6.py <opinion.txt> <phrases.txt> <odd|even|both>
Heads: 'NNN   UNITED STATES v. O'HAGAN' (even pages of 521 U.S.), 'Cite as: ... NNN' (odd pages of 521 U.S.),
'NNN   OCTOBER TERM' / 'DIRKS v. SEC   NNN' (463 U.S.) and '  NNN   Opinion of the Court' (even pages of 463 U.S.).
Output per phrase: the printed page of each line where the phrase starts (first 4 hits).
"""
import re
import sys


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    s = s.replace("­", "")
    s = re.sub(r"[\"'§\[\]*\-]", "", s)
    s = re.sub(r"\s+", "", s)
    return s.lower()


def head_of(line: str) -> int | None:
    if re.match(r"^\s*646\s+(Opinion of the Court|Blac|Bla|Syllabus)", line):
        return None  # 463 U.S. running head carries the case's first page, not the printed page
    m = re.match(r"^\s*(\d{3})\s+(UNITED STATES v\.|OCTOBER TERM|Opinion of the Court|Blac|Bla|Syllabus)", line)
    if m:
        return int(m.group(1))
    m = re.search(r"Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})\s*$", line)
    if m:
        return int(m.group(1))
    m = re.search(r"DIRKS v\. SEC\s+(\d{3})\s*$", line)
    if m:
        return int(m.group(1))
    m = re.search(r"Opinion of the Court\s+463 U\. S\.", line)
    return None


def main() -> None:
    lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().split("\n")
    # cumulative normalized offsets per line
    offs = [0]
    for ln in lines:
        offs.append(offs[-1] + len(norm(ln)))
    full = "".join(norm(ln) for ln in lines)
    # page per line: nearest preceding head, with even-page heads recognised
    cur = None
    page_of: list[int | None] = []
    for ln in lines:
        h = head_of(ln)
        if h is not None:
            cur = h
        m = re.match(r"^\s*(\d{3})\s+\S", ln)
        if m and int(m.group(1)) in range(600, 700) and cur is None:
            cur = int(m.group(1))
        page_of.append(cur)
    for line in open(sys.argv[2], encoding="utf-8"):
        ph = line.rstrip("\n")
        if not ph.strip():
            continue
        n = norm(ph)
        hits = []
        start = 0
        while True:
            k = full.find(n, start)
            if k < 0 or len(hits) >= 4:
                break
            # map offset back to a line index
            li = next(i for i in range(len(lines)) if offs[i] <= k < offs[i + 1]) if k < offs[-1] else len(lines) - 1
            hits.append(f"line{li + 1}:p{page_of[li]}")
            start = k + 1
        print(("FOUND " + " ".join(hits)) if hits else "NOTFOUND", "|", ph[:100])


if __name__ == "__main__":
    main()
