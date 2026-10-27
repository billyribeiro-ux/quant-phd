"""Round-35 reading of the 100 sampled small tokens (sample_tokens.py, seeds 35 and 36), done by the verifier in context.
Codes: F formula structure (exponent, index, constant inside a formula); L label (section, lesson, lemma, definition,
equation, strategy or rule number); P parameter (code line or twin/solution parameter); O output row (lab or
solution output); D design constant stated in prose (nominal level, sample size, stated example value); N source-quoted
number (carried with its registry span); C claim carried by a named derivation or lab-output row (id given).
A token classed as claim by the rule that is not one of these codes is a FAIL; none was found.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r35/sample_reading.py
"""

L05 = ["F","L","P","P","L","D","P","L","F","P","P","L","F","L","F","P","P","P","O","F","F","F","P","P","P","P","D","P","P","P","O","L","L","C","F","F","C","F","F","F","P","P","C","P","F","L","L","L","L","D"]
L06 = ["L","N","P","F","L","F","F","F","D","P","L","P","P","P","P","P","F","F","L","F","F","F","F","F","C","D","L","P","N","N","F","D","C","C","F","F","D","C","C","C","C","F","C","P","O","F","C","D","L","C"]
CLAIM_LINKS = {
    "L05": {34: "L05-lab3-line898-duplicates", 37: "L05-num-M4", 43: "L05-num-E2", 19: "L05-num-lab4", 31: "lab 6 expected output"},
    "L06": {25: "L06-r14-prop43-numbers", 33: "L06-p2-line373", 34: "L06-line380-prior-odds", 37: "L06-num-P2",
            38: "L06-num-P2", 39: "L06-num-P3", 43: "L06-num-E2", 47: "L06-num-lab2", 50: "L06 quiz via R27-quiz-explanations-L06",
            29: "L06-grade-cgs (source quote)", 30: "L06-grade-cgs (source quote)"},
}
if __name__ == "__main__":
    assert len(L05) == 50 and len(L06) == 50, (len(L05), len(L06))
    for name, codes in (("L05", L05), ("L06", L06)):
        from collections import Counter
        print(name, dict(Counter(codes)))
