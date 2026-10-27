"""Check every quoted phrase in L07/L08 that is attributed to Piotroski (2000) against the Ivey-hosted PDF text.
Usage: python3 -I quote_check.py <checkout> <pdf_text_file>"""
import html, re, sys
root, pdf_txt = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", s.replace("­", "")).replace("“", '"').replace("”", '"')
pdf_pages = [norm(p) for p in open(pdf_txt, encoding="utf-8", errors="replace").read().split("\f")]
def find(phrase):
    return [i + 1 for i, p in enumerate(pdf_pages) if norm(phrase) in p]
checks = [
    ("L07 claim line 98 (quote)", "factor analysis may more aptly extract an optimal combination of signals, but such an approach has costs in terms of implementability"),
    ("L07 claim line 102 (quote)", "the stated ex ante implication of each signal is conditioned on the fact that these firms are financially distressed at some level"),
    ("L07 claim line 341 (quote)", "stronger return results than the liquidity metric and aggregate score used in the paper"),
    ("L07 claim line 108 (Sloan passage)", "Sloan [1996] shows that earnings driven by positive accrual adjustments"),
    ("L07 p.6 distress sentence", "The average high BM firm is financially distressed"),
    ("L07 p.12 bootstrap counts", "number of observations equals 1,448 and 396, respectively"),
    ("L07 abstract 7.5%", "can be increased by at least 7.5% annually"),
    ("L07 abstract 23%", "generates a 23% annual return between 1976 and 1996"),
    ("L07 p.7 leverage", "the negative implications of increased leverage seem more plausible than the benefits garnered through a reduction of agency costs"),
    ("L07 p.9 EQOFFER", "did not issue common equity in the year preceding portfolio formation"),
    ("L07 p.7 optimal (fn 2)", "do not represent, nor purport to represent, the optimal set of performance measures"),
    ("L08 misattribution check: Beneish not in Piotroski", "Beneish"),
]
for name, phrase in checks:
    print(f"{name}: pages {find(phrase)}  -> {phrase[:70]}...")
# Exhaustive scan for the words the lesson's generalisations would need
for w in ["outside", "other countr", "other market", "international", "U.S.", "United States", "out-of-sample"]:
    print("PDF contains", repr(w), ":", find(w))
