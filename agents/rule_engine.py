# agents/rule_engine.py

def check_rules(claim):

    disease = claim["disease"].lower().strip()
    days = claim["days"]

    # Diseases excluded if hospitalization <= 3 days
    exclusion_diseases = {
        "asthma": "Clause 19 & 20(i)",
        "bronchitis": "Clause 19 & 20(ii)",
        "chronic nephritis": "Clause 19 & 20(iii)"
    }

    if disease in exclusion_diseases:

        if days <= 3:
            return {
                "decision": "NOT COVERED",
                "reason": f"{disease.title()} treatment not exceeding 3 days is excluded.",
                "clause": exclusion_diseases[disease],
                "confidence": 95
            }

        else:
            return {
                "decision": "POSSIBLY COVERED",
                "reason": f"{disease.title()} hospitalization exceeds 3 days exclusion limit.",
                "clause": exclusion_diseases[disease],
                "confidence": 80
            }

    # Waiting period diseases
    waiting_period_diseases = {
        "cataract": "First Year Waiting Period",
        "hernia": "First Year Waiting Period",
        "hydrocele": "First Year Waiting Period",
        "fistula": "First Year Waiting Period",
        "myomectomy": "First Year Waiting Period",
        "hysterectomy": "First Year Waiting Period",
        "benign prostatic hypertrophy": "First Year Waiting Period"
    }

    if disease in waiting_period_diseases:
        return {
            "decision": "WAITING PERIOD",
            "reason": f"{disease.title()} is subject to first-year waiting period.",
            "clause": waiting_period_diseases[disease],
            "confidence": 90
        }

    return None