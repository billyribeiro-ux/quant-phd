"""SR 26-2 letter and attachment, and CFA Standards pages: quote and page checks for LX2 (run: python3 -I sr_cfa_check.py <scratch/src>).

Sources (plain curl, scratch/src): sr2602.htm (letter), SR2602a1.pdf (attachment, pdftotext per page; the
attachment's printed page equals its PDF page), cfa-iii-a.html, cfa-vi-a.html, cfa-vi-b.html (CFA Standards pages).
"""

import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])


def text_of_html(name: str) -> str:
    s = (src / name).read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).replace("’", "'").replace("‘", "'")


def found(label: str, text: str, needle: str) -> None:
    print(("FOUND     " if needle in text else "NOT FOUND ") + label)


letter = text_of_html("sr2602.htm")
pages = (src / "sr2602a1.txt").read_text(encoding="utf-8", errors="replace")
pdf_pages = (src / "att_raw.txt").read_text(encoding="utf-8", errors="replace").split("\f")
att = re.sub(r"\s+", " ", " ".join(pdf_pages))
print("== SR 26-2 letter")
found("supersedes and replaces SR letter 11-7", letter, "supersedes and replaces SR letter 11-7")
found("SR letter 21-8 named", letter, "SR letter 21-8")
found(
    "applicability over $30 billion",
    letter,
    "expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve",
)
print(
    "hit / bias whole-word count in letter:",
    len(re.findall(r"\bhit\b", letter, flags=re.I)),
    len(re.findall(r"\bbias\b", letter, flags=re.I)),
)
print("== SR 26-2 attachment (footnote marker '1' removed inside the sentence)")
att_clean = att.replace("model 1 risk management", "model risk management")
found(
    "responsibility sentence (pp. 1-2)",
    att_clean,
    "Each banking organization ultimately is responsible for adopting model risk management practices that are appropriate and effective for managing the specific risks the banking organization faces or is likely to face",
)
found(
    "model definition (p. 3; after heading II, before heading III)",
    att,
    "a complex quantitative method, system, or approach that applies statistical, economic, or financial theories to process input data into quantitative estimates",
)
found("simple arithmetic exclusion", att, "simple arithmetic calculations, such as those found within spreadsheets")
found(
    "model risk definition (section III, p. 3)",
    att,
    "the potential for adverse financial consequences associated with models, which may result from decisions made based on model output",
)
found(
    "no enforceable standards (p. 2)",
    att,
    "This guidance does not set forth enforceable standards or prescriptive requirements; accordingly, non-compliance with this guidance will not result in supervisory criticism against a banking organization",
)
found(
    "footnote 1 sentence (p. 2)",
    att,
    "However, supervisory action may result for any violations of law or unsafe or unsound practices stemming from insufficient management of model risk",
)
found("Conceptual Soundness heading (p. 8)", att, "Conceptual Soundness")
found(
    "Outcomes Analysis heading (p. 9)",
    att,
    "Outcomes Analysis Outcomes analysis compares model outputs to corresponding real-world outcomes",
)
found("Ongoing Model Monitoring (p. 9)", att, "Ongoing model monitoring involves an evaluation")
print(
    "hit / bias whole-word count in attachment:",
    len(re.findall(r"\bhit\b", att, flags=re.I)),
    len(re.findall(r"\bbias\b", att, flags=re.I)),
)
print("'Limitations' as a heading (case-sensitive, Limitations):", "Limitations" in att)
print("== CFA Standards")
c3 = text_of_html("cfa-iii-a.html")
c6 = text_of_html("cfa-vi-a.html")
c6b = text_of_html("cfa-vi-b.html")
found(
    "III(A) duty of loyalty",
    c3,
    "Members and candidates have a duty of loyalty to their clients and must act with reasonable care and exercise prudent judgment",
)
found(
    "III(A) often imposed by law",
    c3,
    "often imposed by law or regulation when an individual or institution is charged with the duty of acting for the benefit of another party, such as managing investment assets",
)
found("III(A) minimum benchmark", c3, "establishes a minimum benchmark for the duties of loyalty, prudence, and care")
found("III(A) does not render all fiduciaries", c3, "does not render all members and candidates fiduciaries")
found(
    "III(A) neither impose legal responsibility",
    c3,
    "neither impose such a legal responsibility nor require all members or candidates to act as fiduciaries",
)
found("III(A) must comply with legally imposed duty", c3, "must comply with any legally imposed fiduciary duty")
found(
    "VI(A) definition of conflict",
    c6,
    "any matter that could reasonably be expected to impair independence and objectivity or raise a question about whether actions, judgment, or decision making is free from bias",
)
found(
    "VI(A) best practice avoid", c6, "Best practice is to avoid actual conflicts of interest and the appearance of them"
)
found(
    "VI(A) Example 3 minimum disclosure",
    c6,
    "At minimum, Fargmon must disclose his wife's ownership of Kincaid stock to his employer and in his follow-up report. Best practice is to avoid the conflict by asking his employer to assign another analyst to draft the follow-up report.",
)
found(
    "VI(B) priority of transactions",
    c6b,
    "Investment transactions for clients and employers must have priority over investment transactions in which a member or candidate is the beneficial owner",
)
