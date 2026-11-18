import os, joblib
from src.train_model import train
PATH = "models/model.joblib"
def load():
    if not os.path.exists(PATH): train()
    return joblib.load(PATH)
def predict(text):
    b = load(); p = b["pipeline"].predict_proba([text])[0]
    cls = int(p.argmax())
    return {"class": cls, "label": "Suspicious" if cls == 1 else "Safer-looking", "confidence": float(p[cls]), "p_suspicious": float(p[1])}
