"""Re-check the passages that the automatic matchers reported MISSING, by a phrase search with the printed page.

Usage: python3 -I manual_resolutions.py <src_dir>   (src_dir holds the files written by fetch_sources.sh)
"""

import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])


def norm(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"-\n\s*", "", text)
    return re.sub(r"\s+", " ", text)


def check(label: str, path: str, phrase: str) -> None:
    text = norm(src / path)
    hit = phrase in text
    print(f"{'FOUND  ' if hit else 'ABSENT '} {label}: {phrase[:90]}")


# Statute (GovInfo compilations, text from pdftotext)
s1933 = "comps1884.txt"
s1934 = "comps1885.txt"
check("1934 title (details page; HTML text, not PDF)", "COMPS-1885_details.html", "To provide for the regulation of securities exchanges and of over-the-counter markets")
check("8(d) first sentence, split by a page header in the PDF text", s1933, "issue a stop order suspending the effectiveness of the registration")
check("heading 3 (case-folded)", s1933, "EXEMPTED SECURITIES")
check("heading 4 (case-folded)", s1933, "EXEMPTED TRANSACTIONS")
check("5(d) text (lesson paraphrase drops 'institutions that are')", s1933,
      "qualified institutional buyers or institutions that are accredited investors")
check("15(d)(1) bank count (not quoted in lesson)", s1934, "1,200 persons")

# Opinions: passages with inner quotation marks, bracket alterations, or page breaks
check("Dirks 654 (A-insider sentence, 'secret profits')", "dirks.txt",
      "Thus, an insider will be liable under Rule 10b-5 for inside trading only where he fails to disclose material nonpublic information before trading on it and thus makes")
check("Dirks 654 (mere possession sentence)", "dirks.txt",
      "held that \"a duty to disclose under § 10(b) does not arise from the mere possession of nonpublic market information.\"")
check("Dirks 657 (rooted in the idea)", "dirks.txt", "appears rooted in the idea that the antifraud provisions require equal information among all traders")
check("O'Hagan 651-652 (classical theory)", "ohagan.txt",
      "Under the \"traditional\" or \"classical theory\" of insider trading liability, § 10(b) and Rule 10b-5 are violated when a corporate insider trades in the securities of his corporation")
check("O'Hagan 652 (misappropriation definition)", "ohagan.txt",
      "The \"misappropriation theory\" holds that a person commits fraud \"in connection with\" a securities transaction")
check("O'Hagan n.5 at 653 ('outsider' footnote)", "ohagan.txt",
      "Although an \"outsider\" with respect to Pillsbury, O'Hagan had an intimate association")
check("O'Hagan n.5 at 653 (trader's sanction sentence)", "ohagan.txt",
      "Under the misappropriation theory, O'Hagan's securities trading does not escape Exchange Act sanction")
check("O'Hagan 655 (disclose-to-source limit)", "ohagan.txt",
      "if the fiduciary discloses to the source that he plans to trade on the nonpublic information, there is no \"deceptive device\" and thus no § 10(b) violation")
check("Dirks 663 n.23 (scienter independent element)", "dirks.txt",
      "Scienter-\"a mental state embracing intent to deceive, manipulate, or defraud,\" Ernst & Ernst v. Hochfelder, 425 U. S. 185, 193-194, n. 12 (1976)-is an independent element of a Rule 10b-5 violation.")
check("Dirks 663 body (tipper relevance sentence to which n.23 is attached)", "dirks.txt",
      "Scienter in some cases is relevant in determining whether the tipper has violated his Cady, Roberts duty.")
