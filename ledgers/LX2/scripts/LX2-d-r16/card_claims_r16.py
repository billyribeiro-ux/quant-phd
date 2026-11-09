# Claim assertions for LX2 cards: each assertion pins a fact the verifier read in the lesson, the source or the lab output.
# usage: card_claims_r16.py <cards.json>  -> exit 1 if any assertion fails (used to kill planted card mutants)
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    cards = {c["id"]: c for c in json.load(fh)}

def back(cid):
    return cards[cid]["back"] if cid in cards else ""

def front(cid):
    return cards[cid]["front"] if cid in cards else ""

ASSERTIONS = [
    ("c001 Definition 2.1 identifies section 6(a) and 8(a)", lambda: "section 6(a)" in back("LX2-c001") and "section 8(a)" in back("LX2-c001")),
    ("c004 filed status: section 6(c) fee condition", lambda: "section 6(c)" in back("LX2-c004")),
    ("c009 8(a) twentieth day", lambda: "twentieth day after filing" in back("LX2-c009")),
    ("c010 8(b) ten days both ways", lambda: back("LX2-c010").count("ten days") == 2),
    ("c013 12(d) thirty days", lambda: back("LX2-c013").startswith("Thirty days after")),
    ("c016 15(d)(1) 300 and 1,200 persons", lambda: "less than 300 persons" in back("LX2-c016") and "1,200 persons" in back("LX2-c016")),
    ("c018 R13 listed, R15 not_listed", lambda: "R13 requires the listing to be listed, R15 requires it to be not_listed" in back("LX2-c018")),
    ("c019 R5a effective only; R5c filed or effective", lambda: "R5a permits a sale only when the status is effective" in back("LX2-c019") and "filed or effective" in back("LX2-c019")),
    ("c020 10 states = 5 statuses x 2 listings", lambda: back("LX2-c020").startswith("10: five statuses") and "times two listings" in back("LX2-c020")),
    ("c021 22 transitions = 12 + 10", lambda: "22: six 1933 events" in back("LX2-c021") and "(12)" in back("LX2-c021") and "(10)" in back("LX2-c021")),
    ("c023 two sale-permitted states", lambda: back("LX2-c023").startswith("Two:") and "effective with not_listed and effective with listed" in back("LX2-c023")),
    ("c025 stop order: sale and offer off", lambda: "offer no and sale no" in back("LX2-c025")),
    ("c027 13(a) for registered under section 12; 15(d)(1) for 1933-only", lambda: "Section 13(a) applies to an issuer of a security registered pursuant to section 12" in back("LX2-c027") and "section 15(d)(1)" in back("LX2-c027")),
    ("c028 classical theory pp. 651-652", lambda: "pp. 651-652" in back("LX2-c028")),
    ("c029 temporary fiduciaries quote p. 652", lambda: "O'Hagan, p. 652" in back("LX2-c029") and "temporarily become fiduciaries" in back("LX2-c029")),
    ("c030 tippee assumes duty only when breach and knows or should know (Dirks p. 660)", lambda: "only when the insider has breached" in back("LX2-c030") and "knows or should know" in back("LX2-c030") and "p. 660" in back("LX2-c030")),
    ("c033 personal benefit p. 663", lambda: "reputational benefit that will translate into future earnings" in back("LX2-c033")),
    ("c034 question of fact p. 664", lambda: "“a question of fact,” which “will not always be easy for courts.”" in back("LX2-c034")),
    ("c035 no deceptive device at p. 655", lambda: "no “deceptive device”" in back("LX2-c035")),
    ("c036 consummated without disclosure p. 656", lambda: "When, without disclosure to his principal, the fiduciary uses the information to purchase or sell securities." in back("LX2-c036")),
    ("c037 scienter independent element (n. 23)", lambda: "independent element of a Rule 10b-5 violation" in back("LX2-c037")),
    ("c038 patterns P1, P3, P4, P6 fire", lambda: "P1 (classical branch), P3 and P4 (tippee branch), and P6 (misappropriation branch)" in back("LX2-c038")),
    ("c039 possession is not the duty (p. 654)", lambda: "does not arise from the mere possession" in back("LX2-c039")),
    ("c040 P5 fails knowledge", lambda: "P5 states a personal benefit and fails the knowledge element" in back("LX2-c040")),
    ("c041 no personal gain p. 662", lambda: "Absent some personal gain, there has been no breach of duty to stockholders" in back("LX2-c041")),
    ("c042 duty owed to source p. 652; footnote 5 p. 653", lambda: "(O'Hagan, p. 652)" in back("LX2-c042") and "Footnote 5 (p. 653)" in back("LX2-c042")),
    ("c043 footnote 7 p. 655 n. 7", lambda: "(p. 655 n. 7)" in back("LX2-c043")),
    ("c051 identity G = R + 2X + C_m + C_t", lambda: "G = R + 2X + C_m + C_t" in back("LX2-c051")),
    ("c052 ratio counts events, not shares", lambda: "A trader that cancels one share and a trader that cancels one thousand shares each add 1 to cancels" in back("LX2-c052")),
    ("c053 3 x 97 = 291 < 6 x 104 = 624; 3/104 vs 6/97", lambda: "3 × 97 = 291 is less than 6 × 104 = 624" in back("LX2-c053") and "3/104" in back("LX2-c053") and "6/97" in back("LX2-c053")),
    ("c054 identity needs C_t", lambda: "Without it the right side is short by the shares that traders cancel" in back("LX2-c054")),
    ("c058 zero crossed-book events", lambda: back("LX2-c058").startswith("Zero.") and "events with a crossed book: 0" in back("LX2-c058")),
    ("c059 no trader flagged at threshold 2; 21/37 below 2", lambda: "None." in back("LX2-c059") and "21/37, is below 2" in back("LX2-c059")),
    ("c063 reprice and withdraw both add 1", lambda: back("LX2-c063").startswith("No.") and "Each adds 1 to cancels" in back("LX2-c063")),
    ("c064 Code fiduciary sentence", lambda: "often imposed by law or regulation" in back("LX2-c064")),
    ("c065 Code conflict definition", lambda: back("LX2-c065").startswith("Any matter that could reasonably be expected to impair independence and objectivity")),
    ("c066 model definition excludes spreadsheets", lambda: "such as those found within spreadsheets" in back("LX2-c066")),
    ("c067 model risk definition", lambda: "adverse financial consequences associated with models" in back("LX2-c067")),
    ("c070 hit: inclusive band |e| <= 2", lambda: "|e_t| ≤ 2" in back("LX2-c070") and "inclusive" in back("LX2-c070")),
    ("c071 hit rate denominator H", lambda: "The denominator is the number of periods in the window" in back("LX2-c071")),
    ("c072 bias is mean error", lambda: "bias = (1/H) times the sum of the e_t" in back("LX2-c072")),
    ("c073 ties away from zero, 4 places", lambda: "ties rounded away from zero" in back("LX2-c073") and "10^4" in back("LX2-c073")),
    ("c074 A1 generator ranges", lambda: "−6 to 6 and −4 to 4" in back("LX2-c074")),
    ("c076 Theorem 4.2 at most (monotone)", lambda: "at most the number of hits at b2" in back("LX2-c076") or "is at most the number of hits at b2" in back("LX2-c076")),
    ("c077 Theorem 4.3 bound and equality", lambda: "|bias| ≤" in back("LX2-c077") and "Equality holds if and only if all the errors are ≥ 0 or all the errors are ≤ 0" in back("LX2-c077")),
    ("c078 E[e_t] = 1", lambda: "E[e_t] = 1 index unit" in back("LX2-c078")),
    ("c079 hit probability 44/117 = 0.3761; 8 x 5 + 4", lambda: "44/117, about 0.3761" in back("LX2-c079") and "8 × 5 + 4 = 44" in back("LX2-c079")),
    ("c080 Standard III(A) duty of loyalty", lambda: "A duty of loyalty to clients, with reasonable care and prudent judgment" in back("LX2-c080")),
    ("c081 must comply with legally imposed duty", lambda: "members must comply with any legally imposed one" in back("LX2-c081")),
    ("c082 supersedes SR 11-7 and SR 21-8", lambda: "SR letter 11-7 and SR letter 21-8" in back("LX2-c082")),
    ("c083 over $30 billion", lambda: "over $30 billion in total assets" in back("LX2-c083")),
    ("c085 hit rate 3/8 rounded 0.3750", lambda: "Hit rate 3/8 (9 hits in 24 periods), rounded 0.3750." == back("LX2-c085")),
    ("c086 bias 0 with errors +3 -3 +3 -3; MAE 3", lambda: "+3, −3, +3 and −3" in back("LX2-c086") and "is 3 index units" in back("LX2-c086")),
    ("c087 Example 3 minimum disclosure and best practice", lambda: "disclosure is the minimum" in back("LX2-c087") and "another analyst" in back("LX2-c087")),
    ("c088 III(A) does not render all members fiduciaries", lambda: "“does not render all members and candidates fiduciaries,”" in back("LX2-c088")),
    ("c089 not enforceable; footnote 1", lambda: "“does not set forth enforceable standards or prescriptive requirements,”" in back("LX2-c089") and "will not result in supervisory criticism" in back("LX2-c089")),
    ("c090 Lab 1 reachable 10 of 10", lambda: back("LX2-c090").startswith("10 of 10.")),
    ("c091 both duties 0", lambda: back("LX2-c091").startswith("0. Lab 1 prints 'states where both reporting duties apply: 0'")),
    ("c092 sale-not-offer 0", lambda: back("LX2-c092").startswith("0. Lab 1 prints 'states where a sale is permitted and an offer is not: 0'")),
    ("c093 zero identity failures", lambda: "the count is 0 on the seed-2026 run" in back("LX2-c093")),
    ("c094 zero tally disagreements", lambda: "in 0 trader counts" in back("LX2-c094")),
    ("c095 later of 8(a) date and declaration", lambda: "the 'whichever date is the later' rule of section 8(b)" in back("LX2-c095")),
    ("c096 third sentence excludes year of effectiveness", lambda: back("LX2-c096").startswith("No.") and "excludes that fiscal year" in back("LX2-c096")),
    ("c097 A1 no personal benefit", lambda: "no direct or indirect personal benefit" in back("LX2-c097")),
    ("c098 A2 facts as stated", lambda: "The facts that each pattern states are true" in back("LX2-c098")),
    ("c099 A3 temporary fiduciary must be stated", lambda: "must state that the person is one" in back("LX2-c099")),
    ("c100 bias 41/12 rounded 3.4167", lambda: "Bias 41/12 (errors summing to 82 over 24 periods), rounded 3.4167." == back("LX2-c100")),
    ("c101 Dodd-Frank named, not stated", lambda: "The lesson does not state its provisions" in back("LX2-c101")),
    ("c102 MiFID II named, not stated", lambda: "The lesson does not state its provisions" in back("LX2-c102")),
    ("c104 15(d)(1) second sentence automatic", lambda: back("LX2-c104").startswith("Automatically, if and so long as")),
    ("c105 scienter definition (n. 23)", lambda: "A mental state embracing intent to deceive, manipulate, or defraud" in back("LX2-c105")),
]

failed = []
for label, fn in ASSERTIONS:
    try:
        ok = bool(fn())
    except KeyError:
        ok = False
    if not ok:
        failed.append(label)
print(f"assertions: {len(ASSERTIONS)}; failed: {len(failed)}")
for f in failed:
    print("  FAILED:", f)
sys.exit(1 if failed else 0)
