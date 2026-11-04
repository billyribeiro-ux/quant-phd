"""LX2-d round 1: page locators for the Dirks and O'Hagan quotations on the cards, and statute sentences.

Opinion pages: the reporter page is the last running header (even: 'NNN OCTOBER TERM' / 'NNN UNITED STATES v. O'HAGAN';
odd: 'DIRKS v. SEC NNN' / 'Cite as ... NNN'). Each phrase is searched on three joined lines so line breaks do not hide it.
Statute: the sentence is searched in the whitespace-normalized GovInfo text (page headers inside a sentence are why a
few phrases are split; those are reported as 'split by page header').
Usage: python3 -I opinion_statute_locators.py   (reads /tmp/lx2d-src, see fetch_sources.sh)
"""
import re, sys
sys.path.insert(0, '/tmp/lx2d-src')
from norm import load_pdf_txt, norm

def pages_for(path, header_re):
    lines = load_pdf_txt(path).split('\n')
    cur, pages = None, []
    for ln in lines:
        m = header_re(ln)
        if m:
            cur = int(m)
        pages.append(cur)
    return lines, pages

def dirks_header(ln):
    m = re.match(r'^\s*(\d{3})\s+OCTOBER TERM', ln) or re.search(r'DIRKS v\. SEC\s+(\d{3})\s*$', ln)
    return m.group(1) if m else None

def ohagan_header(ln):
    m = re.match(r'^\s*(\d{3})\s+UNITED STATES v\.', ln) or re.search(r'Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})\s*$', ln)
    return m.group(1) if m else None

def where(lines, pages, phrase):
    out = set()
    phrase = norm(phrase)
    for i in range(len(lines)):
        joined = norm(' '.join(x.strip() for x in lines[i:i + 3]))
        if phrase in joined and pages[i]:
            out.add(pages[i])
    return sorted(out)

D_lines, D_pages = pages_for('/tmp/lx2d-src/USREPORTS-463-646.txt', dirks_header)
O_lines, O_pages = pages_for('/tmp/lx2d-src/USREPORTS-521-642.txt', ohagan_header)
dirks = [
 ('card c041 / lesson p.662', 'Absent some personal gain, there has been no breach of duty to stockholders', '662'),
 ('card c039 / lesson p.654', 'does not arise from the mere possession of nonpublic market information', '654'),
 ('card c040 / lesson p.660', 'a tippee assumes a fiduciary duty to the shareholders', '660'),
 ('card c030 / lesson p.659', "the tippee's duty to disclose or abstain is derivative from that of the insider", '659'),
 ('card c033 / lesson p.663', 'a direct or indirect personal benefit from the disclosure, such as a pecuniary gain', '663'),
 ('card c034 / lesson p.664 (question of fact)', 'a question of fact', '664'),
 ('card c034 / lesson p.664 (not always easy)', 'will not always be easy for courts', '664'),
 ('card c034 / lesson p.664 (gift)', 'an insider makes a gift of confidential information to a trading relative or friend', '664'),
 ('card c037 / lesson p.663 n.23 (scienter)', 'an independent element of a Rule 10b-5 violation', '663'),
 ('card c032 / lesson p.651 n.6 (Section 10(b) text)', 'any manipulative or deceptive device or contrivance', '651'),
]
ohagan = [
 ('card c029 / lesson p.652 (temporary fiduciaries)', 'who temporarily become fiduciaries of a corporation', '652'),
 ('card c028 / lesson pp.651-652 (classical theory)', 'classical theory', '652'),
 ('card c035 / lesson p.655 (disclosure to source)', 'if the fiduciary discloses to the source that he plans to trade', '655'),
 ('card c036 / lesson p.656 (consummation)', 'uses the information to purchase or sell securities', '656'),
 ('card c042 / lesson p.653 n.5 (not an insider)', 'does not escape Exchange Act sanction', '653'),
 ('card c043 / lesson p.655 n.7 (two entities)', 'the trader may still be liable under the misappropriation theory', '655'),
 ('card c043 / lesson p.656 (limits)', 'does not catch all conceivable forms of fraud', '656'),
 ('card c035 / p.655 footnote text present', 'Deception through nondisclosure is central', '654'),
]
bad = 0
for label, phrase, want in dirks:
    got = where(D_lines, D_pages, phrase)
    ok = int(want) in got
    bad += not ok
    print(f"DIRKS {label}: pages found {got} expected {want} {'OK' if ok else 'MISMATCH'}")
for label, phrase, want in ohagan:
    got = where(O_lines, O_pages, phrase)
    ok = int(want) in got
    bad += not ok
    print(f"OHAGAN {label}: pages found {got} expected {want} {'OK' if ok else 'MISMATCH'}")

# statute sentences used by cards (GovInfo COMPS-1884 = 1933 Act, COMPS-1885 = 1934 Act)
S1 = norm(load_pdf_txt('/tmp/lx2d-src/COMPS-1884.txt'))
S2 = norm(load_pdf_txt('/tmp/lx2d-src/COMPS-1885.txt'))
statute = [
 ('c004 6(c) receipt', S1, 'shall be deemed to have taken place upon the receipt thereof'),
 ('c007 5(c) clauses', S1, 'unless a registration statement has been filed as to such security, or while the registration statement is the subject of a refusal order or stop order'),
 ('c009 8(a) twentieth day', S1, 'the effective date of a registration statement shall be the twentieth day after the filing thereof or such earlier date as the commission may determine'),
 ('c010 8(b) trigger (card omits it)', S1, 'if it appears to the commission that a registration statement is on its face incomplete or inaccurate in any material respect'),
 ('c010 8(b) later date', S1, 'whichever date is the later'),
 ('c025 8(d) trigger (card omits it)', S1, 'if it appears to the commission at any time that the registration statement includes any untrue statement of a material fact'),
 ('c025 8(d) cease', S1, 'the stop order shall cease to be effective'),
 ('c011 12(a)', S2, 'to effect any transaction in any security (other than an exempted security) on a national securities exchange unless a registration is effective as to such security for such exchange'),
 ('c013 12(d) thirty days', S2, 'the registration shall become effective thirty days after the receipt of such certification by the commission'),
 ('c014 12(d) withdrawal (card omits the Commission terms clause)', S2, 'upon such terms as the commission may deem necessary to impose for the protection of investors, upon application by the issuer or the exchange to the commission'),
 ('c015 15(d)(1) effective pursuant', S2, 'which has become effective pursuant to the securities act of 1933, as amended'),
 ('c016 15(d)(1) each class (card omits ABS carve-out)', S2, 'the securities of each class, other than any class of asset-backed securities, to which the registration statement relates are held of record by less than 300 persons'),
 ('c016 15(d)(1) other than fiscal year', S2, 'other than the fiscal year within which such registration statement became effective'),
 ('c027 13(a)', S2, 'every issuer of a security registered pursuant to section 12 of this title shall file with the commission'),
]
for label, S, phrase in statute:
    ok = phrase in S
    print(f"STATUTE {label}: {'FOUND' if ok else 'NOT FOUND (see note)'}")
print('locator mismatches:', bad)
