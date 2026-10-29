import re,html,sys
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
s=re.sub(r'<(?=[\s=])','&lt;',s)
s=re.sub(r'(?s)<pre.*?</pre>','[PRE]',s)
s=re.sub(r'<(br|/p|/li|/h\d|/div|/tr|/section)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
print('\n'.join(l.strip() for l in s.split('\n') if l.strip()))
