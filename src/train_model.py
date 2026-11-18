import random, json, joblib, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
random.seed(42)
ORG = ["Alpha Tech", "BrightSoft", "NextGen Labs", "Orion Systems", "Vertex Analytics", "BlueWave", "Cedar IT"]
ROLE = ["software development", "data analysis", "web development", "marketing", "cyber security", "content writing"]
SAFE = [
 "We are pleased to invite you for a technical interview for the {role} internship at {org}. Please bring your college ID card.",
 "Your internship at {org} offers a stipend of Rs. {n} per month. No fees are required at any stage of selection.",
 "Apply through the official careers page of {org}. Selection is based on two interview rounds and a short assignment.",
 "Dear candidate, your offer letter for the {role} role is attached. Please confirm your joining date with HR by email.",
 "{org} is hiring {role} interns. Eligible students can apply on the company website before the deadline.",
 "Your interview for {role} is scheduled on Monday at 11 am via the company meeting link. Kindly confirm your availability.",
 "Thank you for applying to {org}. Shortlisted candidates will be contacted by our recruitment team within two weeks.",
 "The internship duration is {m} months with weekly mentor reviews. A certificate is issued after successful completion.",
]
BAD = [
 "Congratulations! You are selected for the {role} job at {org}. Pay Rs. {fee} registration fee immediately to confirm your seat.",
 "100% job guarantee. Send your bank account number and OTP to receive your joining kit from {org}.",
 "Earn Rs. {big} daily from home. No skills needed. Limited seats, pay now to get started.",
 "Last chance: deposit the security amount of Rs. {fee} today or your offer will be cancelled.",
 "You are already selected at {org}. Transfer Rs. {fee} as training fee now and share your password for the portal.",
 "Guaranteed placement after paying the processing fee of Rs. {fee}. Hurry, offer valid only for {m} hours.",
 "Work from home and make Rs. {big} a day. Easy money, no skills required. Pay the registration amount immediately.",
 "To release your offer letter, send your card number and CVV and pay Rs. {fee} within 24 hours.",
]
def fill(t):
    return t.format(org=random.choice(ORG), role=random.choice(ROLE), n=random.choice([5000, 8000, 10000, 12000, 15000]),
                    m=random.choice([2, 3, 6, 24, 48]), fee=random.choice([500, 1000, 1500, 2000, 2500, 3000]), big=random.choice([3000, 5000, 8000, 10000]))
def build(n_per_class=100):
    rows = []
    for _ in range(n_per_class):
        rows.append((fill(random.choice(SAFE)), 0)); rows.append((fill(random.choice(BAD)), 1))
    df = pd.DataFrame(rows, columns=["text", "label"]).sample(frac=1, random_state=42).reset_index(drop=True)
    return df
def train():
    df = build(); df.to_csv("data/synthetic_offers.csv", index=False)
    Xtr, Xte, ytr, yte = train_test_split(df.text, df.label, test_size=0.25, stratify=df.label, random_state=42)
    pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english")),
                     ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    pipe.fit(Xtr, ytr); pred = pipe.predict(Xte)
    m = {"n_total": len(df), "n_train": len(Xtr), "n_test": len(Xte), "accuracy": accuracy_score(yte, pred),
         "report": classification_report(yte, pred, output_dict=True), "confusion": confusion_matrix(yte, pred).tolist()}
    joblib.dump({"pipeline": pipe, "metrics": m}, "models/model.joblib")
    json.dump(m, open("models/metrics.json", "w"), indent=1)
    return m
if __name__ == "__main__":
    m = train(); print(json.dumps({k: m[k] for k in ["n_total", "n_train", "n_test", "accuracy", "confusion"]}, indent=1))
