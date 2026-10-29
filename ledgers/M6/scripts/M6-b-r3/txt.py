import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
s=re.sub(r'<(br|/p|/li|/h\d|/tr|/div|/section|/pre)[^>]*>','\n',s)
s=re.sub(r'<(?=[A-Za-z/!])[^>]*>','',s)
s=html.unescape(s)
lines=[l.strip() for l in s.split('\n')]
print('\n'.join(l for l in lines if l))
