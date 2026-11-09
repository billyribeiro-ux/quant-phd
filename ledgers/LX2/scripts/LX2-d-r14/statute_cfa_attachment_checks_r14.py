"""Round-14 source checks for LX2 cards (run: python3 -I statute_cfa_attachment_checks_r14.py <src_dir>).

Statute (GovInfo compilations, round-11 text copies): sections 8(b), 8(d), 15(d)(1) third sentence, 12(a),
12(b), 12(d), 2(a)(8). CFA Code (saved HTML converted to text): Standard III(A), VI(A) and Example 3.
SR 26-2 letter and attachment: Supersedes, Applicability, and whole-word search for hit and bias.
Prints FOUND or MISS for each phrase; MISS lines are reported, not hidden.
"""

import html
import re
import sys

src = sys.argv[1]


def norm(s: str) -> str:
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).lower()


def load(name: str) -> str:
    return norm(open(f"{src}/{name}", encoding="utf-8", errors="replace").read())


s1884 = load("c1884.norm.txt")
s1885 = load("c1885.norm.txt")
cfa3 = load("cfa-iii-a.norm.txt")
cfa6 = load("cfa-vi-a.norm.txt")
att = load("att_raw.txt")
sr = load("sr2602a1.txt")
htm = norm(html.unescape(re.sub(r"<[^>]+>", " ", open(f"{src}/sr2602.htm", encoding="utf-8", errors="replace").read())))

# Section 2 only: the definitions in section 2 of the 1933 Act, from 'DEFINITIONS SEC. 2.' to 'SEC. 3.'
_i = s1884.find("definitions sec. 2")
_j = s1884.find("sec. 3.", _i)
SEC2 = s1884[_i:_j]
assert _i > 0 and _j > _i, "section 2 bounds not found"

CHECKS = [
    ("1933 s2(a)(8) registration statement", s1884, "the term ''registration statement'' means the statement provided for in section 6"),
    ("1933 s2 defines no 'in effect' (absence inside section 2 only)", SEC2, "in effect"),
    ("1933 s5(c) clause list", s1884, "unless a registration statement has been filed as to such security, or while the registration statement is the subject of a refusal order or stop order"),
    ("1933 s8(a) twentieth day", s1884, "the twentieth day after the filing thereof or such earlier date as the commission may determine"),
    ("1933 s8(b) ten days notice", s1884, "not later than ten days after the filing of the registration statement"),
    ("1933 s8(b) ten days hearing", s1884, "opportunity for hearing (at a time fixed by the commission) within ten days after such notice"),
    ("1933 s8(b) whichever date is the later", s1884, "whichever date is the later"),
    ("1933 s8(d) fifteen days", s1884, "within fifteen days after such notice"),
    ("1933 s8(d) cease to be effective", s1884, "the stop order shall cease to be effective"),
    ("1933 s8(d) issue a stop order suspending (c025; phrase ends before a page header)", s1884, "issue a stop order suspending the effectiveness of the registration"),
    ("1934 s12(a)", s1885, "effect any transaction in any security (other than an exempted security) on a national securities exchange unless a registration is effective as to such security for such exchange"),
    ("1934 s12(b)", s1885, "may be registered on a national securities exchange by the issuer filing an application with the exchange"),
    ("1934 s12(d) thirty days", s1885, "shall become effective thirty days after the receipt of such certification by the commission or within such shorter period of time as the commission may determine"),
    ("1934 s12(d) withdrawn or stricken", s1885, "may be withdrawn or stricken from listing and registration in accordance with the rules of the exchange"),
    ("1934 s15(d)(1) first sentence", s1885, "which has become effective pursuant to the securities act of 1933, as amended"),
    ("1934 s15(d)(1) second sentence", s1885, "automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12"),
    ("1934 s15(d)(1) third sentence fiscal year", s1885, "other than the fiscal year within which such registration statement became effective"),
    ("1934 s15(d)(1) third sentence 300", s1885, "held of record by less than 300 persons"),
    ("1934 s15(d)(1) third sentence 1,200", s1885, "1,200 persons"),
    ("CFA III(A) duty of loyalty", cfa3, "members and candidates have a duty of loyalty to their clients and must act with reasonable care and exercise prudent judgment"),
    ("CFA III(A) guidance: often imposed", cfa3, "fiduciary duties are often imposed by law or regulation when an individual or institution is charged with the duty of acting for the benefit of another party, such as managing investment assets"),
    ("CFA III(A) legally imposed duty", cfa3, "must comply with any legally imposed fiduciary duty"),
    ("CFA III(A) neither impose", cfa3, "the code and standards neither impose such a legal responsibility nor require all members or candidates to act as fiduciaries"),
    ("CFA VI(A) definition of conflict", cfa6, "a conflict of interest is any matter that could reasonably be expected to impair independence and objectivity or raise a question about whether actions, judgment, or decision making is free from bias"),
    ("CFA VI(A) the standard", cfa6, "members and candidates must avoid or make full and fair disclosure of all matters that could reasonably be expected to impair their independence and objectivity"),
    ("CFA VI(A) best practice avoid", cfa6, "best practice is to avoid actual conflicts of interest and the appearance of them"),
    ("CFA VI(A) Example 3 heading", cfa6, "example 3 (conflict of interest and personal stock ownership)"),
    ("CFA VI(A) Example 3 minimum", cfa6, "at minimum, fargmon must disclose his wife's ownership of kincaid stock to his employer and in his follow-up report"),
    ("CFA VI(A) Example 3 best practice", cfa6, "best practice is to avoid the conflict by asking his employer to assign another analyst to draft the follow-up report"),
    ("SR 26-2 letter supersedes 11-7 and 21-8", htm, "supersedes and replaces sr letter 11-7"),
    ("SR 26-2 letter supersedes 21-8", htm, "sr letter 21-8"),
    ("SR 26-2 letter applicability", htm, "expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the federal reserve"),
    ("attachment model definition", att, "the term \"model\" refers to a complex quantitative method, system, or approach that applies statistical, economic, or financial theories to process input data into quantitative estimates"),
    ("attachment model excludes spreadsheets", att, "excludes simple arithmetic calculations, such as those found within spreadsheets"),
    ("attachment model risk", att, "the term \"model risk\" refers to the potential for adverse financial consequences associated with models, which may result from decisions made based on model output"),
    ("attachment p.1-2 responsible (page break inside)", att, "each banking organization ultimately is responsible for adopting model 1 risk management practices that are appropriate and effective for managing the specific risks the banking organization faces or is likely to face"),
    ("attachment non-enforceable", att, "this guidance does not set forth enforceable standards or prescriptive requirements; accordingly, non-compliance with this guidance will not result in supervisory criticism"),
    ("attachment footnote 1 supervisory action", att, "however, supervisory action may result for any violations of law or unsafe or unsound practices stemming from insufficient management of model risk"),
    ("attachment outcomes analysis definition", att, "outcomes analysis compares model outputs to corresponding real-world outcomes to assess model performance relative to model objectives and business use"),
]
print(f"section 2 length {len(SEC2)} characters")
for label, text, phrase in CHECKS:
    if "absence inside section 2" in label:
        print(("ABSENT " if phrase not in text else "PRESENT") + " " + label)
    else:
        print(("FOUND " if phrase in text else "MISS  ") + label)

for word in ("hit", "bias"):
    n_att = len(re.findall(r"\b" + word + r"\b", att))
    n_sr = len(re.findall(r"\b" + word + r"\b", sr))
    n_htm = len(re.findall(r"\b" + word + r"\b", htm))
    print(f"word search '{word}': attachment {n_att}, SR letter pdf text {n_sr}, letter html {n_htm}")
