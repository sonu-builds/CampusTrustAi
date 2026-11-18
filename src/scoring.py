from src.prediction import predict
from src.risk_engine import analyse
def score(text):
    ml = predict(text); r = analyse(text)
    final = 0.55 * ml["p_suspicious"] * 100 + 0.45 * r["rule_score"]
    level = "HIGH" if final >= 60 else "MEDIUM" if final >= 30 else "LOW"
    return {"ml": ml, "rules": r, "final": round(final, 1), "level": level}
