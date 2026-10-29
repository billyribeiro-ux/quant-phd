import html,re,sys
src=open(sys.argv[1],encoding='utf-8').read()
src=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',src)
src=re.sub(r'(?i)</(p|li|h[1-6]|div|tr|pre|dt|dd|section|blockquote)>|<br\s*/?>',r'\n',src)
src=re.sub(r'</?[a-zA-Z!][^<>]*>','',src)
src=html.unescape(src)
for i,l in enumerate([x.strip() for x in src.split('\n')],1):
    if l: print(i,l)
