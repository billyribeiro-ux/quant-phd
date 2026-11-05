"""Check the quoted statute phrases in L01 and cards against the normalised GovInfo PDF text.

Usage: python3 -I statute_check.py <dir holding c1884.norm.txt and c1885.norm.txt>
"""
import sys
import os

d = sys.argv[1]
s33 = open(os.path.join(d, 'c1884.norm.txt'), encoding='utf-8').read()
s34 = open(os.path.join(d, 'c1885.norm.txt'), encoding='utf-8').read()
checks = [
    (s33, 'Except as hereinafter provided, the effective date of a registration statement shall be the twentieth day after the filing thereof or such earlier date as the Commission may determine'),
    (s33, 'after notice by personal service or the sending of confirmed telegraphic notice not later than ten days after the filing of the registration statement, and opportunity for hearing (at a time fixed by the Commission) within ten days after such notice'),
    (s33, 'the registration shall become effective at the time provided in subsection (a) or upon the date of such declaration, whichever date is the later'),
    (s33, 'the stop order shall cease to be effective'),
    (s33, 'after notice by personal service or the sending of confirmed telegraphic notice, and after opportunity for hearing (at a time fixed by the Commission) within fifteen days after such notice'),
    (s34, 'shall also be automatically suspended as to any fiscal year, other than the fiscal year within which such registration statement became effective'),
    (s34, 'held of record by less than 300 persons, or, in the case of a bank, a savings and loan holding company'),
    (s34, '1,200 persons'),
    (s34, 'the registration shall become effective thirty days after the receipt of such certification by the Commission or within such shorter period of time as the Commission may determine'),
    (s34, 'upon application by the issuer or the exchange to the Commission; whereupon the issuer shall be relieved'),
    (s33, 'emerging growth company’’ means an issuer'),
]
for src, phrase in checks:
    print('FOUND' if phrase in src else 'MISSING', '|', phrase[:90])
