import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?s)<script.*?</script>','',s)
s=re.sub(r'(?s)<style.*?</style>','',s)
s=re.sub(r'(?i)<br\s*/?>','\n',s)
s=re.sub(r'(?i)</(p|li|h[1-6]|tr|div|section|article|pre|table)>','\n',s)
s=re.sub(r'</?[a-zA-Z!][^>]*>','',s)
s=html.unescape(s)
out=[l.strip() for l in s.split('\n')]
print('\n'.join(l for l in out if l))
