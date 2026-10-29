import re, sys
# usage: letters.py <file> <letter> [letter...]: list lines where a single letter appears as a math token or subscript
path = sys.argv[1]
letters = sys.argv[2:]
text = open(path, encoding="utf-8").read().splitlines()
for ln, line in enumerate(text, 1):
    for seg in re.findall(r"\\\((.*?)\\\)", line):
        for L in letters:
            if re.search(r"(?<![A-Za-z\\])" + re.escape(L) + r"(?![A-Za-z])", seg) or re.search(r"(?<![A-Za-z\\])" + re.escape(L) + r"_", seg):
                print(f"{ln}: {L} in \\({seg[:110]}\\)")
                break
