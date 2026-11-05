"""Statute, opinion, CFA and SR 26-2 quote and locator checks for LX2 (run: python3 -I statute_check.py <scratch/src>).

Inputs are the plain-curl sources in <scratch>/src: COMPS-1884/1885 (pdftotext, normalised), the Dirks and O'Hagan
PDFs, the CFA Standards HTML pages, and the SR 26-2 attachment PDF. Prints FOUND / NOT FOUND per quoted sentence and
the printed page for the statute sentences and the attachment pages.
"""

import re
import sys
import html
from pathlib import Path

src = Path(sys.argv[1])


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s)


def check(label: str, text: str, needle: str) -> None:
    print(("FOUND    " if needle in text else "NOT FOUND") + "  " + label)


c84 = norm((src / "c1884.txt").read_text(encoding="utf-8", errors="replace"))
c85 = norm((src / "c1885.txt").read_text(encoding="utf-8", errors="replace"))
print("== 1933 Act (COMPS-1884)")
check(
    "8(b) ten days / hearing within ten days",
    c84,
    "within ten days after such notice by personal service or the sending of such telegraphic notice",
)
check(
    "8(d) hearing 'within fifteen days' (statute condition)",
    c84,
    "and after opportunity for hearing (at a time fixed by the Commission) within fifteen days after such notice",
)
check("8(d) stop order ceases to be effective", c84, "the stop order shall cease to be effective")
check(
    "8(e) examination sentence",
    c84,
    "make an examination in any case in order to determine whether a stop order should issue under subsection (d)",
)
check("2(a)(19) EGC definition", c84, "(19) The term ''emerging growth company'' means an issuer")
check("2(a)(5) Commission", c84, "(5) The term ''Commission'' means the Securities and Exchange Commission")
check(
    "5(d) EGC communications",
    c84,
    "may engage in oral or written communications with potential investors that are qualified institutional buyers",
)
check(
    "6(e)(1) confidential nonpublic review",
    c84,
    "for confidential nonpublic review by the staff of the Commission prior to public filing",
)
check(
    "6(e)(1) 15 days before road show",
    c84,
    "publicly filed with the Commission not later than 15 days before the date on which the issuer conducts a road show",
)
check("EXEMPTED SECURITIES heading (sec 3)", c84, "EXEMPTED SECURITIES")
check("EXEMPTED TRANSACTIONS heading (sec 4)", c84, "EXEMPTED TRANSACTIONS")
print("== 1934 Act (COMPS-1885)")
check(
    "12(a) quote",
    c85,
    "to effect any transaction in any security (other than an exempted security) on a national securities exchange unless a registration is effective as to such security for such exchange",
)
check(
    "12(b) quote",
    c85,
    "A security may be registered on a national securities exchange by the issuer filing an application with the exchange",
)
check(
    "12(d) thirty days",
    c85,
    "the registration shall become effective thirty days after the receipt of such certification by the Commission",
)
check(
    "12(d) withdrawn or stricken",
    c85,
    "may be withdrawn or stricken from listing and registration in accordance with the rules of the exchange",
)
check("15(d)(1) first sentence", c85, "which has become effective pursuant to the Securities Act of 1933, as amended")
check(
    "15(d)(1) second sentence",
    c85,
    "The duty to file under this subsection shall be automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12",
)
check("15(d)(1) third sentence, 300-persons ground", c85, "held of record by less than 300 persons")
check(
    "15(d)(1) third sentence, bank clause (1,200 persons)",
    c85,
    "in the case of a bank, a savings and loan holding company (as defined in section 10 of the Home Owners' Loan Act), or a bank holding company, as such term is defined in section 2 of the Bank Holding Company Act of 1956 (12 U.S.C. 1841), 1,200 persons",
)
