import re, sys, json
src_dir = sys.argv[1]
def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('­', '')
    s = re.sub(r'-\s*\n\s*', '', s)            # join hyphenated line breaks
    s = re.sub(r'\s+', ' ', s)
    return s.strip()
def load(name):
    return norm(open(f'{src_dir}/{name}', encoding='utf-8', errors='replace').read())
dirks = load('dirks.txt')
ohagan = load('ohagan.txt')
comps84 = load('comps1884.txt')
comps85 = load('comps1885.txt')
checks = {
 'dirks_655_tippee': (dirks, 'Unlike insiders who have independent fiduciary duties to both the corporation and its shareholders, the typical tippee has no such relationships.'),
 'dirks_660_test': (dirks, 'Thus, a tippee assumes a fiduciary duty to the shareholders of a corporation not to trade on material nonpublic information only when the insider has breached his fiduciary duty to the shareholders by disclosing the information to the tippee and the tippee knows or should know that there has been a breach.'),
 'dirks_fn23_scienter': (dirks, 'a mental state embracing intent to deceive, manipulate, or defraud'),
 'ohagan_652_temporary': (ohagan, 'not only to officers, directors, and other permanent insiders of a corporation, but also to attorneys, accountants, consultants, and others who temporarily become fiduciaries of a corporation.'),
 'sec8d_stop_order': (comps84, 'issue a stop order suspending the effectiveness of the registration statement'),
 'sec8d_cease': (comps84, 'the stop order shall cease to be effective'),
 'sec8d_fifteen': (comps84, 'after opportunity for hearing (at a time fixed by the Commission) within fifteen days after such notice by personal service or the sending of such telegraphic notice, issue a stop order'),
 'sec15d_second': (comps85, 'The duty to file under this subsection shall be automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12 of this title.'),
 'sec15d_third_300_1200': (comps85, 'as to any fiscal year, other than the fiscal year within which such registration statement became effective, if, at the beginning of such fiscal year, the securities of each class, other than any class of asset-backed securities, to which the registration statement relates are held of record by less than 300 persons, or, in the case of a bank, a savings and loan holding company (as defined in section 10 of the Home Owners’ Loan Act), or a bank holding company, as such term is defined in section 2 of the Bank Holding Company Act of 1956 (12 U.S.C. 1841), 1,200 persons'),
}
for k,(hay,needle) in checks.items():
    n = norm(needle)
    print(k, n in hay, hay.count(n))
