# agents/output_agent.py

import json

def create_output(
    disease,
    days,
    decision,
    reason,
    clause,
    confidence
):

    output = {
        "disease": disease,
        "hospitalization_days": days,
        "decision": decision,
        "reason": reason,
        "clause": clause,
        "confidence": confidence
    }

    return json.dumps(
        output,
        indent=4
    )