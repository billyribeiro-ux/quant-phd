"""Statute-text checks for the LX2 slice a L01 claims, against the GovInfo compilations fetched by fetch_sources.sh.

Usage: python3 -I statute_checks.py <scratch dir with comps1884.txt and comps1885.txt>
Each check prints the observed line numbers or text so that the verifier fragment can cite them.
"""
import re
import sys

src = sys.argv[1]
c84 = open(f"{src}/comps1884.txt", encoding="utf-8", errors="replace").read().split('\n')
c85 = open(f"{src}/comps1885.txt", encoding="utf-8", errors="replace").read().split('\n')


def find(lines, pattern):
    return [(i + 1, ln.strip()[:150]) for i, ln in enumerate(lines) if re.search(pattern, ln)]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


print("1. 'in effect' in 1933 Act section 2 (comps1884.txt lines 34-391):")
hits = [(i, ln) for i, ln in find(c84, r"in effect") if 34 <= i <= 391]
print("   hits:", hits)
print("   'SEC. 2.' at", find(c84, r"SEC\. 2\. ")[:1], " 'SEC. 3.' at", find(c84, r"SEC\. 3\. ")[:1])
print("2. 5(a) opening (comps1884.txt):", find(c84, r"SEC\. 5\. .*Unless a registration statement is in effect")[:1])
print("3. 5(d) limitation for emerging growth companies:", find(c84, r"LIMITATION")[:3])
print("4. 6(e)(1) road show phrase:", find(c84, r"road show")[:2])
print("5. 8(b) lines:", find(c84, r"^\s+\(b\) If it appears to the Commission that a registration")[:1])
print("   8(b) refusing / whichever date:", find(c84, r"refusing to permit such statement|whichever date is the later")[:3])
print("6. 8(d) lines:", find(c84, r"\(d\) If it appears to the Commission at any time")[:1])
print("   8(d) suspending / cease to be effective:", find(c84, r"suspending the effectiveness|cease to be effective")[:3])
print("7. 8(e) empowered:", find(c84, r"hereby empowered")[:1])
print("8. 2(a)(5) Commission definition:", find(c84, r"means the Securities and Ex")[:1])
print("9. 15(d)(1) third sentence (comps1885.txt):")
print("   suspended as to any fiscal year:", find(c85, r"suspended as to any fis")[:1])
print("   asset-backed exclusion:", find(c85, r"other than any class of$")[:1])
print("   held of record by less than 300:", find(c85, r"held of record by less than 300")[:1])
print("   bank count 1,200:", find(c85, r"1,200 persons")[:1])
print("10. 'national securities exchange' defined in 1934 Act section 3(a) (comps1885.txt lines 100-260):")
print("   definitions in 3(a) lines 100-400 naming a term:", [(i, t) for i, t in find(c85, r"The term") if 100 <= i <= 400][:12])
print("   'national securities exchange' with 'means' in lines 100-400:", [x for x in find(c85, r"national securities exchange.{0,20}means") if 100 <= x[0] <= 400])
print("11. Amended Through lines:", find(c84, r"As Amended Through P\.L\. 119.27")[:1], find(c85, r"As Amended Through P\.L\. 119.60")[:1])
