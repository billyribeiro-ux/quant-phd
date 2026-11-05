"""Check the statute phrases the LX2 cards and lessons quote, against the COMPS-1884 and COMPS-1885 text.

Usage: python3 -I statute_phrases.py <comps1884.norm.txt> <comps1885.norm.txt>
The two inputs are made by norm_statute.py from pdftotext -layout dumps of the GovInfo PDFs (fetched by plain curl
on 2026-11-04; sha256 of COMPS-1884.pdf c67e553505b0329d..., COMPS-1885.pdf c7a620b624baa99b...).
Each phrase is printed with FOUND or NOT FOUND, and the sentence it sits in is printed for the timing clauses.
"""

import re
import sys

comps84 = open(sys.argv[1], encoding="utf-8").read()
comps85 = open(sys.argv[2], encoding="utf-8").read()
checks = [
    ("8(b) notice timing (card c010, L01 line 84)", comps84, "after notice by personal service or the sending of confirmed telegraphic notice not later than ten days after the filing of the registration statement"),
    ("8(b) hearing timing (card c010)", comps84, "opportunity for hearing (at a time fixed by the Commission) within ten days after such notice"),
    ("8(d) hearing timing (card c025, L01 lines 85 and 378)", comps84, "opportunity for hearing (at a time fixed by the Commission) within fifteen days after such notice"),
    ("8(d) stop order wording", comps84, "issue a stop order suspending the effectiveness of the registration statement"),
    ("8(d) cease clause (card c025)", comps84, "the Commission shall so declare and thereupon the stop order shall cease to be effective"),
    ("8(b) later-of rule (card c095)", comps84, "whichever date is the later"),
    ("5(c) clauses (card c007)", comps84, "unless a registration statement has been filed as to such security, or while the registration statement is the subject of a refusal order or stop order or (prior to the effective date of the registration statement) any public proceeding or examination under section 8"),
    ("12(a) (card c011)", comps85, "to effect any transaction in any security (other than an exempted security) on a national securities exchange unless a registration is effective as to such security for such exchange"),
    ("12(d) thirty days (card c013)", comps85, "the registration shall become effective thirty days after the receipt of such certification by the Commission or within such shorter period of time as the Commission may determine"),
    ("12(d) withdrawal (card c014)", comps85, "A security registered with a national securities exchange may be withdrawn or stricken from listing and registration in accordance with the rules of the exchange and, upon such terms as the Commission may deem necessary to impose for the protection of investors, upon application by the issuer or the exchange to the Commission"),
    ("15(d)(1) fiscal-year sentence with bank count (card c016)", comps85, "held of record by less than 300 persons, or, in the case of a bank, a savings and loan holding company (as defined in section 10 of the Home Owners’ Loan Act), or a bank holding company, as such term is defined in section 2 of the Bank Holding Company Act of 1956 (12 U.S.C. 1841), 1,200 persons"),
    ("15(d)(1) excludes the effective fiscal year (card c096)", comps85, "other than the fiscal year within which such registration statement became effective"),
]
for label, text, phrase in checks:
    normalised = re.sub(r"\s+", " ", phrase)
    print(("FOUND    " if normalised in text else "NOT FOUND") + f"  {label}")
