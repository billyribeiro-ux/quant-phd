import re,sys,html
s=open(sys.argv[1]).read()
s=re.sub(r'<script.*?</script>','',s,flags=re.S)
s=re.sub(r'<style.*?</style>','',s,flags=re.S)
s=re.sub(r'</?(p|li|h[1-6]|div|section|tr|dd|dt|figure|blockquote|ol|ul|table)[^>]*>',r'\n',s)
s=re.sub(r'</?[a-zA-Z][^>]*>','',s)
s=html.unescape(s)
print('\n'.join(l.rstrip() for l in s.split('\n') if l.strip()))
