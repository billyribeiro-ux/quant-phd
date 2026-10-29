import sys, re, html
src = sys.argv[1]
s = open(src, encoding="utf-8").read()
s = re.sub(r"<(?![/!]?(?:p|em|h[1-6]|span|div|section|a|details|summary|code|pre|ol|ul|li|table|thead|tbody|tr|th|td|strong|sup|sub|button|svg|input|label|script|figure|figcaption|select|option|header|nav|main|article|br|img|dfn|style|canvas|body|head|meta|link|title|html|footer|aside|dl|dt|dd|blockquote|hr|i|b|kbd)[\s>/])", "&lt;", s)
s = re.sub(r"(?s)<script.*?</script>", "", s)
s = re.sub(r"(?s)<style.*?</style>", "", s)
s = re.sub(r"(?i)<br\s*/?>", "\n", s)
s = re.sub(r"(?i)</(p|li|h[1-6]|div|tr|section|pre)>", "\n", s)
s = re.sub(r"<[^>]+>", "", s)
s = html.unescape(s)
for i, line in enumerate([l for l in s.split("\n") if l.strip()], 1):
    print(f"{i}: {line}")
