# Reference review queue: research run, 2026-10-27

41 items from `references/review_queue.json` (28 articles, 8 primary documents, 5 books) were researched by three
read-only Haiku agents. Method: find an authoritative record you can cite (Crossref, OpenAlex, publisher or issuer page
on `references/authorities.yaml`), then run `tools/add_reference.py ... --dry-run`. Nothing was written to
`references/`, the matcher in `tools/refs/match.py` was not touched, no bot check, login or paywall was bypassed.

**Result: 0 admissible, 14 not admissible, 6 blocked, 21 no record.**

Patterns a person can act on:
- Pre-1999 AER / JEL / HBR / Risk / Wilmott articles have no DOI in Crossref or OpenAlex; the AEA host serves a bot check and
  hbr.org is not on the allow-list. They stay in the queue as honest gaps unless a human admits a stable publisher URL.
- Three books need a decision about the citation string or the source record, not the matcher: Kindleberger & Aliber (7th ed.,
  2015) (the authoritative record lists Aliber first), Koller et al. (7th ed.) (Open Library's author field is "Inc."), McCloskey
  (title similarity 0.72 against the 0.75 threshold).
- FASB ASC, SEC and Bank of England pages refuse the tool (for the Bank of England page plain curl returns 200 while the
  tool gets 403: worth a human look); the Cboe white paper and the SEC rule are PDFs, which the URL route cannot admit.

Per-item decisions with the verbatim dry-run output and the evidence (URLs and quoted lines) are in
`plans/reference-queue-research-2026-10-27.json`.

| Source | Verdict | Route | Why / what a person must decide |
|---|---|---|---|
| Drepper (2007), 'What Every Programmer Should Know About Memory' | no_record | none | Honest gap. Cannot be admitted by any allowed route. |
| MacKinlay (1997), 'Event Studies in Economics and Finance', Journal of Economic Literature 35(1 | no_record | url | Venue has no DOI for 1997; only the RePEc/e-jel copy exists, which is not an allowed route. AEA page behind a bot check. |
| Grossman & Stiglitz (1980), 'On the Impossibility of Informationally Efficient Markets', AER 70 | not_admissible | doi | The only DOI found is a Columbia Academic Commons DOI that Crossref does not hold; the tool cannot admit it. AER 1980 has no Crossref DOIs. |
| Friedman (1968), 'The Role of Monetary Policy', AER 58(1) | not_admissible | doi | The only Crossref hit is a Routledge reader chapter that reprints the article. The matcher rejects it (no authors, different container). AER 1968 has no Crossref DOIs (Cr |
| Gagnon, Raskin, Remache & Sack (2011), International Journal of Central Banking 7(1) | not_admissible | url | Publisher domain is allowed but the page lacks Highwire citation_* tags, which the publishers route requires. |
| Rey (2013), Jackson Hole Economic Policy Symposium | no_record | url | Honest gap. Only a PDF copy exists on an allowed domain and it is unreachable; a PDF cannot satisfy the publishers meta requirement. The citation string also has no title |
| McLeay, Radia & Thomas (2014), Bank of England Quarterly Bulletin Q1 | blocked | url | The tool's fetch gets HTTP 403. Not worked around (no UA change). Also the page carries no citation_* tags, and the citation has no title words for the issuer route. Expe |
| Porter (1979), 'How Competitive Forces Shape Strategy', Harvard Business Review 57(2) | no_record | none | Honest gap. HBR is not an allowed publisher and no DOI was found. |
| Cooper & Kaplan (1988), 'Measure Costs Right: Make the Right Decisions', Harvard Business Revie | no_record | none | Honest gap. HBR not an allowed domain; the Crossref hit is a different publication. The [V] flag is unrelated to admission. |
| Modigliani & Miller (1958), 'The Cost of Capital, Corporation Finance and the Theory of Investm | no_record | none | Honest gap. AER 1958 has no DOI in Crossref or OpenAlex; the only allowed route would be AEA, which is behind a bot check. |
| Modigliani & Miller (1963), 'Corporate Income Taxes and the Cost of Capital: A Correction', AER | no_record | none | Honest gap. No DOI and no allowed route; AEA page behind bot check (pubs.aeaweb.org 403). |
| Lintner (1956), 'Distribution of Incomes of Corporations Among Dividends, Retained Earnings, an | no_record | none | Honest gap. No DOI; only non-allowed copy found. |
| Jensen (1986), 'Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers', AER 76(2) | no_record | none | Honest gap. No DOI in Crossref or OpenAlex; CiteSeerX copy is not an allowed route. |
| Bengen (1994), Journal of Financial Planning 7(4) | no_record | none | Honest gap. Journal of Financial Planning is not on an allowed domain and has no DOI in either index. |
| Fama & Bliss (1987), 'The Information in Long-Maturity Forward Rates', AER 77(4) | no_record | none | Real AER article but no DOI in any allowed source; URL route needs an article page on aeaweb.org with citation_* meta, none found. |
| Hagan, Kumar, Lesniewski & Woodward (2002), Wilmott Magazine | no_record | none | Wilmott 2002 issue article not located; Wiley is not an allowed publisher domain. |
| Shiller (1981), 'Do Stock Prices Move Too Much to be Justified by Subsequent Changes in Dividen | not_admissible | doi | The only DOI found is NBER Working Paper w0456, a different publication. AER 71(3) article not located in Crossref or OpenAlex. |
| Dupire (1994), Risk 7(1) | no_record | none | Risk 7(1) not registered in Crossref or OpenAlex. |
| Giles & Glasserman (2006), Risk | no_record | none | No record located for the 2006 Risk article. |
| Breiman (1961), Proceedings of the Fourth Berkeley Symposium, Vol. 1 | not_admissible | doi | The DTIC report is a different publication (1962 report). Proceedings of the Fourth Berkeley Symposium are on Project Euclid, not an allowed domain. |
| Almgren, Thum, Hauptmann & Li (2005), Risk | no_record | none | Risk article has no DOI in Crossref or OpenAlex; no allowed-domain page. |
| Rogoff (1996), 'The Purchasing Power Parity Puzzle', JEL 34(2) | no_record | none | JEL article without DOI; e-jel.org is not in authorities.yaml. Crossref returned no 1996 JEL record. |
| Working (1949), 'The Theory of Price of Storage', AER 39(6) | no_record | none | AER 39(6) article not located in any source. |
| Brennan (1958), 'The Supply of Storage', AER 48(1) | no_record | none | AER 48(1) article not located in any source. |
| Duffie (2020), 'Still the World's Safe Haven?', Hutchins Center Working Paper 62 [V] | no_record | none | Hutchins Center WP 62 page not located on brookings.edu (allowed publisher domain); flag V unresolved. Honest gap. |
| Bernanke (1983), 'Nonmonetary Effects of the Financial Crisis in the Propagation of the Great D | not_admissible | doi | Neither candidate is the AER article. |
| Cochrane (2005), 'Writing Tips for Ph.D. Students' (note) | no_record | none | Unpublished web note; no DOI and no allowed-domain page. The author's own site is not in authorities.yaml. |
| Klein (2007), 'Performing a Project Premortem', Harvard Business Review 85(9) | not_admissible | doi | The IEEE reprint is a different publication from HBR 85(9); HBR not an allowed route. |
| Graham & Dodd, Security Analysis (1934) | not_admissible | isbn | No allowed route admits the 1934 first edition. The matcher judged the 1996 reprint record and rejected it on year (window is one year). |
| FASB Accounting Standards Codification (primary) | blocked | url | Bot check on the FASB host. Not bypassed. No command can be given until a fasb.org page is reachable through the tool. |
| Koller, Goedhart & Wessels, Valuation, 7th ed. (2020) | not_admissible | isbn | Open Library's author for this ISBN is 'Inc.' (malformed author data), so the first-author rule fails. No Crossref DOI for the 2020 edition was found. Not forced. |
| FASB Accounting Standards Codification Topic 815, Derivatives and Hedging (primary) | blocked | url | Blocked host. No sub-page was fetched because the host itself refuses access. |
| Bank of England, Financial Stability Report on the 2022 LDI episode (primary) [V] | blocked | url | The tool's fetch is refused while a curl fetch succeeds. I did not change the User-Agent or any other header to get past the refusal. The title 'Financial Stability Repor |
| SEC T+1 settlement rule (primary) | blocked | url | SEC rate-limit block. Not bypassed. Retry after a long wait, at a slower rate, with an unchanged User-Agent. The release's title 'Shortening the Securities Settlement Cyc |
| Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) | not_admissible | isbn | No record dated 1989 to 1993 was returned by any route, so the one-year window fails. The 2nd edition record in Open Library lists 1991, but the ISBN lookup the tool perf |
| Cboe VIX methodology white paper (primary) | not_admissible | url | The official VIX methodology documents are PDFs. The URL route reads an HTML <title> and cannot read a PDF title, so no PDF can be admitted by this route. The fallback ti |
| ALFRED real-time database, Federal Reserve Bank of St. Louis (primary) | not_admissible | url | ALFRED's page titles contain 'ALFRED' and 'St. Louis Fed' but not 'real-time database', so recall stays at 33%. The citation's product name does not match any title the s |
| SEC, Standards for Covered Clearing Agencies for U.S. Treasury Securities (2023) (primary) | blocked | url | SEC rate-limit block, same as the T+1 item. Even if reachable, a PDF cannot pass the URL route's HTML title check (see Cboe item). So the likely outcome is not_admissible |
| Kindleberger & Aliber, Manias, Panics, and Crashes, 7th ed. (2015) | not_admissible | doi | The record is the right book and year, but Crossref lists Aliber as first author. The citation names Kindleberger first, so the first-author rule rejects it. The citation |
| SEC v. Texas Gulf Sulphur Co., 401 F.2d 833 (2d Cir. 1968) | no_record | none | No case.law (Caselaw Access Project) page was found, so the allowed route has no URL to fetch. Opinion copies on other hosts are not authoritative under the registry's po |
| McCloskey, Economical Writing, 3rd ed. (2019) | not_admissible | isbn | The record is the right book, author and year. The title is 'Economical Writing, Third Edition' against a citation title of 'Economical Writing', so the title similarity  |
