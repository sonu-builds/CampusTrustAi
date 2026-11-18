import streamlit as st, pandas as pd, plotly.express as px
from src.scoring import score
from src import database as db
st.set_page_config(page_title="CampusTrust AI", page_icon="🛡️", layout="wide")
db.init()
page = st.sidebar.radio("Navigation", ["Overview", "Offer Analyzer", "Scan History", "Admin Dashboard"])
st.sidebar.caption("Decision-support prototype. Not proof of fraud or of a genuine offer.")
ADVICE = ["Verify the company on its official website and MCA/LinkedIn pages.", "Never pay a fee or share OTP, passwords or bank details to get an offer.",
          "Contact the company through an independently found phone number or email.", "Ask your placement cell or a senior before responding."]
if page == "Overview":
    st.title("🛡️ CampusTrust AI")
    st.subheader("AI-powered internship and job offer risk screening")
    st.write("Paste an internship or job-offer message. CampusTrust AI combines a TF-IDF + Logistic Regression classifier with transparent rule checks to highlight **suspicious indicators** and suggest verification steps.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Model", "TF-IDF + LR"); c2.metric("Rule indicators", "6"); c3.metric("Storage", "SQLite")
    st.info("A LOW result is never proof that an offer is genuine. Always verify independently.")
elif page == "Offer Analyzer":
    st.title("Offer Analyzer")
    text = st.text_area("Paste offer text", height=150, key="offer")
    if st.button("Analyze Offer", type="primary"):
        if not text.strip():
            st.warning("Please paste some offer text to analyse.")
        else:
            r = score(text)
            db.insert(text, r["ml"]["label"], r["ml"]["confidence"], int(round(r["final"])), r["level"], r["rules"]["indicators"])
            col = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}[r["level"]]
            c1, c2, c3 = st.columns(3)
            c1.metric("Risk category", f"{col} {r['level']}"); c2.metric("Heuristic score", f"{r['final']} / 100")
            c3.metric("ML class (confidence)", f"{r['ml']['label']} ({r['ml']['confidence']*100:.1f}%)")
            st.write("**Detected indicators:** " + (", ".join(r["rules"]["indicators"]) or "none"))
            st.write(f"Rule score: {r['rules']['rule_score']}  |  ML suspicious probability: {r['ml']['p_suspicious']*100:.1f}")
            st.write("**Recommended verification steps**")
            for a in ADVICE: st.write("- " + a)
elif page == "Scan History":
    st.title("Scan History"); df = db.fetch()
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Download CSV", df.to_csv(index=False), "scan_history.csv", "text/csv")
else:
    st.title("Admin Dashboard"); df = db.fetch()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total scans", len(df)); c2.metric("High-risk scans", int((df.risk_level == "HIGH").sum())); c3.metric("Average score", f"{df.risk_score.mean():.1f}")
    a, b = st.columns(2)
    cnt = df.risk_level.value_counts().reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0).reset_index(); cnt.columns = ["Risk level", "Scans"]
    a.plotly_chart(px.bar(cnt, x="Risk level", y="Scans", color="Risk level", color_discrete_map={"LOW": "#548235", "MEDIUM": "#ED7D31", "HIGH": "#C00000"}, title="Scans by risk level"), use_container_width=True)
    b.plotly_chart(px.histogram(df, x="risk_score", nbins=10, title="Score distribution"), use_container_width=True)
