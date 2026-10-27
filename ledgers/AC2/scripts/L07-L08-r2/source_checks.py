"""Round-2 source checks for L07 and L08 (AC2): quotes and locators against the Ivey-hosted
Piotroski (2000) PDF, and the constants and threshold against the Wikipedia page, both fetched
with plain curl (see the commands in the fragment). Run: python3 -I source_checks.py <src_dir>
where <src_dir> holds piotroski.pdf and wiki.txt (plain text of the Wikipedia article)."""
import re
import subprocess
import sys
import os

src = sys.argv[1]
pdf = os.path.join(src, "piotroski.pdf")
raw = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True, check=True).stdout
pages = raw.split("\f")
norm = lambda s: re.sub(r"\s+", " ", s)

def page_of(phrase):
    return [i + 1 for i, p in enumerate(pages) if phrase in norm(p)]

checks = {
    "p.1 abstract 7.5%": "increased by at least 7.5% annually",
    "p.1 abstract 23%": "generates a 23% annual return between 1976 and 1996",
    "p.3 7.5% repeat": "can be increased by at least 7.5% annually",
    "p.3 23% repeat": "generates a 23% annual return between 1976 and 1996",
    "p.6 average high BM distressed": "The average high BM firm is financially distressed",
    "p.7 conditioning quote (full sentence)": "the stated ex ante implication of each signal is conditioned on the fact that these firms are financially distressed at some level",
    "p.7 leverage clause": "the negative implications of increased leverage seem more plausible than the benefits garnered through a reduction of agency costs",
    "p.7 n.2 factor analysis quote": "factor analysis may more aptly extract an optimal combination of signals, but such an approach has costs in terms of implementability",
    "p.7 ROA/CFO beginning-of-year scaling": "scaled by beginning-of-the-year total assets",
    "p.8 Sloan accrual sentence": "Sloan [1996] shows that earnings driven by positive accrual adjustments",
    "p.8 FTACCRUAL CFO>ROA": "equals one if CFO> ROA",
    "p.8 leverage avg assets": "total long-term debt to average total assets",
    "p.8 source of funds heading": "Leverage, Liquidity, and Source of",
    "p.9 EQOFFER did not issue": "did not issue common equity in the year preceding portfolio formation",
    "p.9 fn5 cutoff 1.5": "A specification where the current ratio cutoff equals 1.5 yields stronger return results than the liquidity metric and aggregate score used in the paper",
    "p.9 ATURN scaled by BoY assets": "total sales scaled by beginning-of-the-year total assets",
    "p.10 composite score section": "2.3.4. Composite Score",
    "p.11 1976-1996 sample": "Each year between 1976 and 1996",
    "p.11 prior-year BM distribution": "The prior fiscal year's BM distribution is used to classify firms into BM quintiles",
    "p.11-12 beginning of the fifth month": "beginning of the fifth month after the firm's",
    "p.12 1,448 and 396 bootstrap": "number of observations equals 1,448 and 396, respectively",
    "p.12 8 or 9 high / 0 or 1 low": "FSCOREequals 0 or 1",
    "p.1 size/turnover/analyst (R2)": "small and medium-sized firms, companies with low share turnover, and firms with no analyst following",
}
for label, phrase in checks.items():
    print(f"{label}: pdf pages {page_of(phrase)}")
print("'U.S.' occurrences after the journal cover line:",
      sum(len(re.findall(r"U\.S\.", norm(p))) for i, p in enumerate(pages) if i > 0))
print("'Printed in US.A.' on p.1 only:", "Printed in US.A." in norm(pages[0]))

wiki = open(os.path.join(src, "wiki.txt"), encoding="utf-8").read()
for label, pat in [("equation line", r"M-score = −4\.84 \+ 0\.92 × DSRI \+ 0\.528 × GMI \+ 0\.404 × AQI \+ 0\.892 × SGI \+ 0\.115 × DEPI −0\.172 × SGAI \+ 4\.679 × TATA − 0\.327 × LVGI"),
                   ("threshold -1.78", r"threshold value is -1\.78"),
                   ("4.697 absent", r"4\.697"), ("-2.22 absent", r"2\.22")]:
    print(f"wikipedia {label}: {len(re.findall(pat, wiki))} match(es)")
