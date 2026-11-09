import re,sys
from pathlib import Path
root=Path(sys.argv[1])
bad=0
for f in ['course/modules/LX/LX1/L03.html','course/modules/LX/LX1/L04.html']:
    src=(root/f).read_text(encoding='utf-8')
    segs=re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', src, re.S)
    for a,b in segs:
        s=a or b
        s=re.sub(r'\\text\{[^}]*\}','',s)
        n=re.findall(r'(?<![A-Za-z\\])T(?![A-Za-z])', s)
        if n:
            bad+=len(n); print(f, s[:120])
print('bare T inside TeX math segments in L03+L04 (text stripped):', bad)
