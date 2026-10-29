import sys,re,html
p=sys.argv[1]
s=open(p,encoding='utf-8').read()
s=re.sub(r'<script.*?</script>','',s,flags=re.S)
s=re.sub(r'<style.*?</style>','',s,flags=re.S)
s=re.sub(r'<(br|/p|/li|/h\d|/div|/pre|/tr|/dd|/dt)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
lines=[l.strip() for l in s.split('\n') if l.strip()]
print('\n'.join(lines))
