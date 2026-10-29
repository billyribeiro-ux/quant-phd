import re,sys,html
src=open(sys.argv[1],encoding='utf-8').read()
src=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',src)
src=re.sub(r'(?i)</(p|li|h[1-6]|div|tr|section|table)>','\n',src)
src=re.sub(r'(?i)<br\s*/?>','\n',src)
src=re.sub(r'<[^>]+>','',src)
src=html.unescape(src)
lines=[l.strip() for l in src.split('\n')]
out=[]
for i,l in enumerate(lines):
    if l: out.append(f"{i}: {l}")
print('\n'.join(out))
