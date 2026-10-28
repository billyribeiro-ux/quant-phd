import re,html,sys
raw=open(sys.argv[1],encoding='utf-8').read()
raw=re.sub(r'<script.*?</script>|<style.*?</style>',' ',raw,flags=re.S)
raw=re.sub(r'<br\s*/?>|</p>|</li>|</h\d>|</pre>','\n',raw)
t=html.unescape(re.sub(r'<[^>]+>','',raw))
t=re.sub(r'[ \t]+',' ',t)
print(re.sub(r'\n\s*\n+','\n',t))
