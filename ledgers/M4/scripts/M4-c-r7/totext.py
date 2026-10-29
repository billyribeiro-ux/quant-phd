import re,sys,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?is)<script.*?</script>|<style.*?</style>','',s)
s=re.sub(r'(?i)<(br|/p|/li|/h\d|/tr|/div|/pre|/section)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
lines=[l.rstrip() for l in s.split('\n')]
out=[]
for i,l in enumerate(lines):
    if l.strip(): out.append(f"{i+1}: {l.strip()}")
print('\n'.join(out))
