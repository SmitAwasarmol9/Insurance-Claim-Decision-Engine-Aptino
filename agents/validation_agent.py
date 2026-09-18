# agents/validation_agent.py

def validate_claim(claim):

    if not claim["disease"]:
        return False

    if claim["days"] <= 0:
        return False

    return True