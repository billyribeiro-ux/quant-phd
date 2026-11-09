"""Locate printed pages of quoted passages in the Dirks and O'Hagan texts (round-11 extractions).

Usage: python3 -I page_locate_r14.py <src_dir>
In the raw text a standalone three-digit line 6xx that follows the running head ("DIRKS v. SEC" or
the page header) is the printed U.S. Reports page on which the following text starts. For each phrase
the script searches the raw text (any whitespace between words, curly and straight quotes equivalent)
and reports the last page-number line that starts before the match: that is the page the phrase is on.
"""
import re
import sys

src = sys.argv[1]
CHECKS = {
    "dirks.txt": [
        ("Dirks n.6 operative text", "any manipulative or deceptive device or contrivance", "651 n.6"),
        ("Dirks p.654 mere possession", "does not arise from the mere possession of nonpublic market information", "654"),
        ("Dirks p.654 fiduciary relationship", "arises rather from the existence of a fiduciary relationship", "654"),
        ("Dirks p.657 equal information", "appears rooted in the idea that the antifraud provisions require equal information", "657"),
        ("Dirks p.659 tippee derivative", "the tippee's duty to disclose or abstain is derivative from that of the insider's duty", "659"),
        ("Dirks p.659 always free", "does not mean that such tippees always are free to trade on the information", "659"),
        ("Dirks p.660 tippee test", "a tippee assumes a fiduciary duty to the shareholders of a corporation not to trade", "660"),
        ("Dirks p.662 purpose", "depends in large part on the purpose of the disclosure", "662"),
        ("Dirks p.662 absent personal gain", "Absent some personal gain, there has been no breach of duty to stockholders", "662"),
        ("Dirks p.663 personal benefit", "a direct or indirect personal benefit from the disclosure", "663"),
        ("Dirks p.663 n.23 scienter", "an independent element of a Rule 10b-5 violation", "663 n.23"),
        ("Dirks p.664 gift", "gift of confidential information to a trading relative or friend", "664"),
        ("Dirks p.664 question of fact", "a question of fact", "664"),
        ("Dirks p.664 not always easy", "will not always be easy for courts", "664"),
        ("Dirks p.655 unlike insiders", "Unlike insiders who have independent fiduciary duties", "655"),
        ("Dirks p.672 dissent trust", "relationship of trust and confidence between the insider and the shareholder", "672"),
        ("Dirks p.676 n.13 cynical", "somewhat cynical view, gifts involve personal gain", "676 n.13"),
    ],
    "ohagan.txt": [
        ("OH classical theory", "Under the traditional or classical theory of insider trading liability", "651-652"),
        ("OH p.652 classical quote", "applies not only to officers, directors, and other permanent insiders", "652"),
        ("OH p.652 misappropriation", "The misappropriation theory holds that a person commits fraud", "652"),
        ("OH n.5 not insider", "was not an insider of", "653 n.5"),
        ("OH n.5 escape", "does not escape Exchange Act sanction", "653 n.5"),
        ("OH p.654 deception nondisclosure", "Deception through nondisclosure is central", "654"),
        ("OH p.655 disclose plans", "if the fiduciary discloses to the source that he plans to trade", "655"),
        ("OH p.655 n.7 two entities", "the trader may still be liable under the misappropriation theory", "655 n.7"),
        ("OH p.656 uses the information", "uses the information to purchase or sell securities", "656"),
        ("OH p.656 does not catch all", "does not catch all conceivable forms of fraud", "656"),
        ("OH p.656 coincide", "The securities transaction and the breach of duty thus coincide", "656"),
        ("OH p.679 Scalia", "must be construed to require the manipulation or deception of a party", "679"),
        ("OH p.680 Thomas", "fails to provide a coherent and consistent interpretation", "680"),
    ],
}
for fname, items in CHECKS.items():
    raw = open(f"{src}/{fname}", encoding="utf-8", errors="replace").read()
    raw_n = raw.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    marks = []
    for m in re.finditer(r"(?m)^\s*(6\d\d)\s*$", raw_n):
        marks.append((m.start(), m.group(1)))
    for label, phrase, claimed in items:
        words = phrase.split()
        pat = r"\s+".join(re.escape(w) for w in words)
        hits = list(re.finditer(pat, raw_n))
        if not hits:
            print(f"{fname} | {label} | claimed p.{claimed} | NOT FOUND (whitespace-tolerant)")
            continue
        pages = []
        for m in hits:
            page = None
            for off, p in marks:
                if off <= m.start():
                    page = p
            pages.append(page)
        print(f"{fname} | {label} | claimed p.{claimed} | matches on pages {pages}")
