import streamlit as st
import json

from agents.validation_agent import validate_claim
from agents.retrieval_agent import retrieve_policy
from agents.rule_engine import check_rules
from agents.decision_agent import make_decision
from agents.output_agent import create_output

st.set_page_config(
    page_title="Insurance Claim Decision Engine",
    page_icon="🏥",
    layout="wide"
)

# ---------- CUSTOM CSS ----------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(90deg,#0f172a,#1e293b);
    color: white;
    margin-bottom: 20px;
}

.metric-box {
    padding: 15px;
    border-radius: 12px;
    background-color: #111827;
    border: 1px solid #374151;
    text-align: center;
}

.small-text {
    font-size: 14px;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------

with st.sidebar:

    st.title("🏥 Insurance AI")

    st.markdown("""
### Features

✅ Multi-Agent System

✅ ChromaDB RAG

✅ Rule Engine

✅ LLM Decision Agent

✅ JSON Output

✅ FastAPI Backend

---

Built using:

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- Groq LLM
""")

# ---------- HERO ----------

st.markdown("""
<div class="hero">
<h1>🏥 Insurance Claim Decision Engine</h1>
<p>RAG + Multi-Agent AI System for Automated Insurance Claim Evaluation</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUTS ----------

col1, col2 = st.columns(2)

with col1:
    disease = st.text_input(
        "Disease",
        placeholder="Example: Asthma"
    )

with col2:
    days = st.number_input(
        "Hospitalization Days",
        min_value=1,
        step=1
    )

# ---------- BUTTON ----------

if st.button("🚀 Evaluate Claim", use_container_width=True):

    claim = {
        "disease": disease,
        "days": days
    }

    if not validate_claim(claim):

        st.error("Invalid Claim Data")
        st.stop()

    query = f"""
    Disease: {disease}
    Hospitalization Days: {days}
    """

    with st.spinner("Analyzing policy and evaluating claim..."):

        policy_text = retrieve_policy(query)

        rule_result = check_rules(claim)

    st.divider()

    # ---------- CLAIM SUMMARY ----------

    st.subheader("📋 Claim Summary")

    st.info(
        f"Disease: {disease}\n\nHospitalization Days: {days}"
    )

    # ---------- POLICY EVIDENCE ----------

    with st.expander("📖 View Retrieved Policy Evidence"):

        st.write(policy_text[:3000])

    st.divider()

    # ---------- RULE ENGINE ----------

    if rule_result:

        decision = rule_result["decision"]
        reason = rule_result["reason"]
        clause = rule_result["clause"]
        confidence = rule_result["confidence"]

        st.subheader("🎯 Final Decision")

        if decision == "COVERED":
            st.success(f"✅ {decision}")

        elif decision == "NOT COVERED":
            st.error(f"❌ {decision}")

        elif decision == "WAITING PERIOD":
            st.warning(f"⚠️ {decision}")

        else:
            st.info(decision)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Decision", decision)

        with c2:
            st.metric("Confidence", f"{confidence}%")

        with c3:
            st.metric("Clause", clause)

        st.markdown("### Reason")
        st.write(reason)

        st.markdown("### Confidence Score")
        st.progress(confidence)

        json_output = create_output(
            disease,
            days,
            decision,
            reason,
            clause,
            confidence
        )

        st.download_button(
            "📄 Download JSON Report",
            json_output,
            file_name="claim_report.json",
            mime="application/json"
        )

    # ---------- LLM PATH ----------

    else:

        result = make_decision(
            claim,
            policy_text
        )

        if isinstance(result, dict):

            decision = result.get("decision", "UNKNOWN")
            reason = result.get("reason", "No reason provided")
            confidence = result.get("confidence", 80)

        else:

            decision = "LLM ANALYSIS"
            reason = str(result)
            confidence = 80

        st.subheader("🤖 LLM Decision")

        st.success(f"✅ {decision}")

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

        st.write(reason)

        st.progress(confidence)