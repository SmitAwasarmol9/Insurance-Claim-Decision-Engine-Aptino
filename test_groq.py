from agents.decision_agent import make_decision

claim = {
    "disease": "asthma",
    "days": 2
}

policy_text = """
Treatment of Asthma not exceeding three days is excluded.
"""

result = make_decision(
    claim,
    policy_text
)

print(result)