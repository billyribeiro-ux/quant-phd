import re,sys,html
L=sys.argv[1]; start=sys.argv[2]; end=sys.argv[3]; pat=sys.argv[4] if len(sys.argv)>4 else None
t=open(f'course/modules/M/M2/{L}.html',encoding='utf-8').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=re.sub(r'</?(p|li|h[1-6]|div|section|tr|dd|dt)[^>]*>','\n',t)
t=html.unescape(re.sub(r'<[^>]+>','',t))
t=re.sub(r'[ \t]+',' ',t)
a=t.find(start); b=t.find(end,a+1) if end!='-' else len(t)
seg=t[a:b]
for line in seg.split('\n'):
    if line.strip() and (pat is None or re.search(pat,line)): print(line.strip()[:700])
