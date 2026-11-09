import re,sys,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
s=re.sub(r'<(p|li|h2|h3|h4|h5|tr|div|pre|section|details|summary)[^>]*>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
lines=[l.strip() for l in s.split('\n')]
lines=[l for l in lines if l]
print('\n'.join(lines))
