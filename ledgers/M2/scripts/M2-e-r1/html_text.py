import re, sys, html
def text(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(re.sub(r'\s+', ' ', s))
if __name__ == '__main__':
    pat = re.compile(sys.argv[2], re.I)
    t = text(sys.argv[1])
    for m in pat.finditer(t):
        print('...', t[max(0, m.start()-160):m.end()+160], '...\n')
