import re
RULES = {
    "Upfront fee": (35, r"(registration|security|training|processing|joining|course|kit)\s*(fee|amount|deposit|charges?)|pay\s+(rs\.?|₹|inr)?\s*[\d,]+|deposit\s+(the\s+)?(security|amount)|refundable\s+(fee|amount)"),
    "Urgent payment": (18, r"(pay|deposit|transfer)[^.]{0,30}(immediately|today|now|urgent)|last chance|within\s+\d+\s+hours|offer will be cancelled"),
    "Guaranteed selection": (15, r"100\s*%\s*(selection|job|placement)|guaranteed\s+(job|selection|placement)|job guarantee|you are (already )?selected"),
    "Sensitive credentials": (35, r"\botp\b|password|bank account|card number|\bcvv\b|\bpin\b|aadhaar"),
    "Unrealistic daily pay": (12, r"(earn|make)\s+(rs\.?|₹)?\s*[\d,]{4,}\s*(per day|daily|a day)"),
    "Vague easy-money claims": (10, r"no skills? (needed|required)|work from home|earn from home|easy money|limited (seats|slots)"),
}
def analyse(text: str):
    t = text.lower()
    hits, score = [], 0
    for name, (w, pat) in RULES.items():
        if re.search(pat, t):
            hits.append(name); score += w
    score = min(score, 100)
    level = "HIGH" if score >= 60 else "MEDIUM" if score >= 30 else "LOW"
    return {"indicators": hits, "rule_score": score, "rule_level": level}
