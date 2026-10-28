import re,sys,html
path=sys.argv[1]; start=int(sys.argv[2]); end=int(sys.argv[3])
lines=open(path).read().split('\n')
for i in range(start-1,min(end,len(lines))):
    t=re.sub(r'<[^>]+>','',lines[i]); t=html.unescape(t).strip()
    if t: print(i+1, t[:1500])
