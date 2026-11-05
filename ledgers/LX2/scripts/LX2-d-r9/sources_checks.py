"""Check the SR 26-2, CFA Standards and SR 26-2 attachment quotations the LX2 cards cite (LX2-d round 9).

Usage: python3 -I ledgers/LX2/scripts/LX2-d-r9/sources_checks.py <scratch-src-dir>
Inputs (fetched by plain curl on 2026-11-04 into <scratch-src-dir>): sr2602.htm (federalreserve.gov SR 26-2),
SR2602a1.pdf (attachment, read with pdftotext -layout into sr2602a1.txt), cfa-iii-a.txt and cfa-vi-a.txt (the
CFA Institute standards pages at the canonical URLs .../standards-of-practice-iii-a and .../standards-of-practice-vi-a,
tags stripped). Prints FOUND or NOT FOUND for each quoted phrase, and counts the whole-word 'hit' and 'bias'.
"""

import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
sr_html = (src / "sr2602.htm").read_text(encoding="utf-8", errors="replace")
sr_html = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", sr_html)
sr_text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", sr_html)))
att = re.sub(r"\s+", " ", (src / "sr2602a1.txt").read_text(encoding="utf-8", errors="replace"))
cfa3 = re.sub(r"\s+", " ", (src / "cfa-iii-a.txt").read_text(encoding="utf-8", errors="replace"))
cfa6 = re.sub(r"\s+", " ", (src / "cfa-vi-a.txt").read_text(encoding="utf-8", errors="replace"))

checks = [
    ("letter: supersedes and replaces SR 11-7 and SR 21-8 (card c082)", sr_text, "supersedes and replaces SR letter 11-7"),
    ("letter: Supersedes list (card c082)", sr_text, "Supersedes: SR letter 11-7"),
    ("letter: Applicability over $30 billion (card c083)", sr_text, "This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve."),
    ("attachment: model definition (card c066)", att, "a complex quantitative method, system, or approach that applies statistical, economic, or financial theories to process input data into quantitative estimates"),
    ("attachment: excludes simple arithmetic (card c066)", att, "simple arithmetic calculations, such as those found within spreadsheets"),
    ("attachment: model risk definition (card c067)", att, "the potential for adverse financial consequences associated with models, which may result from decisions made based on model output"),
    ("attachment: responsibility sentence (card c068)", att, "Each banking organization ultimately is responsible for adopting model risk management practices that are appropriate and effective for managing the specific risks the banking organization faces or is likely to face"),
    ("attachment: outcomes analysis (card c069)", att, "Outcomes analysis compares model outputs to corresponding real-world outcomes to assess model performance relative to model objectives and business use."),
    ("attachment: no enforceable standards (card c089)", att, "This guidance does not set forth enforceable standards or prescriptive requirements; accordingly, non-compliance with this guidance will not result in supervisory criticism"),
    ("attachment: footnote 1 sentence (card c089)", att, "However, supervisory action may result for any violations of law or unsafe or unsound practices stemming from insufficient management of model risk."),
    ("CFA III(A): duty of loyalty (card c080)", cfa3, "Members and candidates have a duty of loyalty to their clients and must act with reasonable care and exercise prudent judgment"),
    ("CFA III(A): often imposed (card c064)", cfa3, "Fiduciary duties are often imposed by law or regulation when an individual or institution is charged with the duty of acting for the benefit of another party, such as managing investment assets."),
    ("CFA III(A): neither impose (card c081, c088)", cfa3, "the Code and Standards neither impose such a legal responsibility nor require all members or candidates to act as fiduciaries"),
    ("CFA III(A): does not render all members (card c088)", cfa3, "Standard III(A) does not render all members and candidates fiduciaries"),
    ("CFA III(A): legally imposed duty (card c081)", cfa3, "members and candidates must comply with any legally imposed fiduciary duty"),
    ("CFA VI(A): conflict definition (card c065)", cfa6, "A conflict of interest is any matter that could reasonably be expected to impair independence and objectivity or raise a question about whether actions, judgment, or decision making is free from bias."),
    ("CFA VI(A): avoid or disclose (card c087)", cfa6, "Members and candidates must avoid or make full and fair disclosure of all matters that could reasonably be expected to impair their independence and objectivity"),
    ("CFA VI(A): best practice (card c087)", cfa6, "Best practice is to avoid actual conflicts of interest and the appearance of them."),
    ("CFA VI(A): Example 3 outcome (card c087)", cfa6, "At minimum, Fargmon must disclose his wife’s ownership of Kincaid stock to his employer and in his follow-up report. Best practice is to avoid the conflict by asking his employer to assign another analyst to draft the follow-up report."),
]
for label, text, phrase in checks:
    print(("FOUND     " if phrase in text else "NOT FOUND ") + label)
for word in ("hit", "bias"):
    print(f"whole-word '{word}' in attachment: {len(re.findall(rf'\b{word}\b', att, re.I))}; in letter: {len(re.findall(rf'\b{word}\b', sr_text, re.I))}")
