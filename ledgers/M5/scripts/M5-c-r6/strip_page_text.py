import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)
s=re.sub(r'</(p|li|h[1-6]|tr|div|pre|section|dd|dt)>','\n',s)
s=re.sub(r'<br\s*/?>','\n',s)
s=re.sub(r'</?[a-zA-Z][^>]*>','',s)
s=html.unescape(s)
out=[]
for i,l in enumerate(s.split('\n'),1):
    if l.strip(): out.append(f"{i}: {l.strip()}")
print('\n'.join(out))
