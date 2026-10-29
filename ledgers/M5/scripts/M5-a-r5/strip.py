import re,sys,html
t=open(sys.argv[1]).read()
a,b=int(sys.argv[2]),int(sys.argv[3])
lines=t.split('\n')[a-1:b]
s='\n'.join(lines)
s=re.sub(r'</?(span|p|em|strong|div|li|ul|ol|h\d|section|code|dfn|a|table|tr|td|th|label|input|fieldset|legend|details|summary|sup|sub|br|pre|thead|tbody|img|i|b|section)\b[^>]*>','',s)
s=html.unescape(s)
for l in s.split('\n'):
    if l.strip(): print(l.strip()[:3000])
