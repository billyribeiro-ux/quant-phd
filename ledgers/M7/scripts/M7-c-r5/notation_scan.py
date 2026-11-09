import re, collections, sys
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    cmds = collections.Counter(re.findall(r'\\[A-Za-z]+', s))
    print(f, dict(cmds))
    segs = re.findall(r'\\\((.*?)\\\)', s, re.S) + re.findall(r'\\\[(.*?)\\\]', s, re.S)
    letters = collections.Counter()
    for seg in segs:
        seg2 = re.sub(r'\\[A-Za-z]+', ' ', seg)
        for m in re.findall(r'(?<![A-Za-z])[A-Za-z](?![A-Za-z])', seg2):
            letters[m] += 1
    print('single letters in math:', sorted(letters.items()))
