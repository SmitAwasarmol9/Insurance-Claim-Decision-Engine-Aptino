from fastapi import FastAPI
from pydantic import BaseModel

from agents.validation_agent import validate_claim
from agents.retrieval_agent import retrieve_policy
from agents.rule_engine import check_rules
from agents.decision_agent import make_decision

app = FastAPI(
    title="Insurance Claim Decision Engine API"
)

class ClaimRequest(BaseModel):
    disease: str
    days: int


@app.get("/")
def home():
    return {
        "message": "Insurance Claim Decision Engine API Running"
    }


@app.post("/evaluate")
def evaluate_claim(data: ClaimRequest):

    claim = {
        "disease": data.disease,
        "days": data.days
    }

    if not validate_claim(claim):
        return {
            "error": "Invalid Claim"
        }

    query = f"""
    Disease: {claim['disease']}
    Hospitalization Days: {claim['days']}
    """

    policy_text = retrieve_policy(query)

    rule_result = check_rules(claim)

    if rule_result:
        return rule_result

    result = make_decision(
        claim,
        policy_text
    )

    return {
        "llm_result": result
    }