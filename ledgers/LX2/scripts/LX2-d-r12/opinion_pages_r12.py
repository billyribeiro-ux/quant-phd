"""Map quoted passages of O'Hagan (521 U.S. 642) and Dirks (463 U.S. 646) to printed pages (round 12).
Page starts: O'Hagan body pages from the '521US2 NNN' running heads and '(1997) NNN' page markers; Dirks from
the 'NNN OCTOBER TERM' / 'DIRKS v. SEC NNN' running heads. Positions are approximate to the page."""
import re
SRC = '/Users/billyribeiro/.fanout/scratch-LX2-d-r11/src/'
def page_index(t2, pats):
    marks = []
    for p in pats:
        for m in re.finditer(p, t2):
            marks.append((m.start(), int(m.group(1))))
    marks.sort()
    def at(pos):
        cur = None
        for p, n in marks:
            if p <= pos:
                cur = n
            else:
                break
        return cur
    return at
ot = re.sub(r'\s+', ' ', open(SRC + 'ohagan.txt', encoding='utf-8', errors='replace').read())
oat = page_index(ot, [r'521US2 (\d{3})', r'\(1997\) (\d{3}) '])
for q in ['classical theory applies not only to officers', 'Under the “traditional” or “classical theory”',
          'misappropriates confidential information for securities trading purposes',
          'in breach of a duty owed to the source of the information', 'does not escape Exchange Act sanction',
          'the trader may still be liable under the misappropriation theory',
          'discloses to the source that he plans to trade', 'without disclosure to his principal',
          'O’Hagan was not an “insider” of Pillsbury', 'there is no “deceptive device”']:
    hits = [m.start() for m in re.finditer(re.escape(q), ot)]
    print('O\'Hagan', repr(q[:60]), [(h, oat(h)) for h in hits] or 'NOT FOUND')
dt = re.sub(r'\s+', ' ', open(SRC + 'dirks.txt', encoding='utf-8', errors='replace').read())
dat = page_index(dt, [r'(?<![\d.,])(6[4-7]\d)(?= (?:OCTOBER TERM|DIRKS v\. SEC|Opinion of the Court|Syllabus))',
                      r'(?:DIRKS v\. SEC|DIRKS v\. SECURITIES AND EXCHANGE COMMISSION) (6[4-7]\d)(?= )'])
for q in ['a duty to disclose under § 10(b) does not arise from the mere possession of nonpublic market information',
          'Absent some personal gain, there has been no breach of duty to stockholders',
          'knows or should know that there has been a breach', 'a direct or indirect personal benefit from the disclosure',
          'an independent element of a Rule 10b-5 violation', 'The elements of fiduciary duty and exploitation',
          'will not always be easy for courts']:
    hits = [m.start() for m in re.finditer(re.escape(q), dt)]
    print('Dirks', repr(q[:60]), [(p, dat(p)) for p in hits])
