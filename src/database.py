import sqlite3
DB = "scans.db"
def init(path=DB):
    c = sqlite3.connect(path)
    c.execute("""CREATE TABLE IF NOT EXISTS scans(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 offer_text TEXT, ml_prediction TEXT, ml_confidence REAL, risk_score INTEGER, risk_level TEXT, indicators TEXT)""")
    c.commit(); c.close()
def insert(offer, pred, conf, score, level, ind, path=DB):
    c = sqlite3.connect(path)
    c.execute("INSERT INTO scans(offer_text,ml_prediction,ml_confidence,risk_score,risk_level,indicators) VALUES (?,?,?,?,?,?)",
              (offer, pred, conf, score, level, ", ".join(ind))); c.commit(); c.close()
def fetch(path=DB):
    import pandas as pd
    c = sqlite3.connect(path); df = pd.read_sql("SELECT * FROM scans ORDER BY id DESC", c); c.close(); return df
