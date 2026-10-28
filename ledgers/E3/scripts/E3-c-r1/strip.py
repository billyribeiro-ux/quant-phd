import re,sys,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
m=re.search(r'(?s)<main.*</main>',s)
if m: s=m.group(0)
s=re.sub(r'(?i)<(br|/p|/li|/h[1-6]|/div|/section|/tr|/table|/pre)[^>]*>','\n',s)
s=re.sub(r'<[a-zA-Z/!][^>]*>','',s)
s=html.unescape(s)
out=[]
for i,l in enumerate(s.split('\n')):
    if l.strip(): out.append(f"{i}: {l.strip()}")
print("\n".join(out))
