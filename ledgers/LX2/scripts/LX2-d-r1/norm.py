import re, html, sys
def load_pdf_txt(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'-\n\s*', '', s)            # de-hyphenate line breaks
    s = s.replace('\f', ' ')
    s = re.sub(r'ø[^¿]*¿', ' ', s)            # GovInfo bracket markup
    return s
def load_html_txt(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))
def norm(s):
    s = s.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    s = s.replace('‘‘', '"').replace('’’', '"').replace("''", '"')
    s = s.replace('–', '-').replace('—', '-').replace('−', '-').replace(' ', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()
