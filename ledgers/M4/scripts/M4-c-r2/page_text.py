import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'<script.*?</script>','',s,flags=re.S)
s=re.sub(r'<style.*?</style>','',s,flags=re.S)
s=re.sub(r'<(br|/p|/li|/h[1-6]|/tr|/div|/pre|/section)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
s=re.sub(r'\n\s*\n+','\n',s)
print(s)
