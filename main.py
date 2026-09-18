from agents.case_agent import get_claim
from agents.validation_agent import validate_claim
from agents.retrieval_agent import retrieve_policy
from agents.decision_agent import make_decision
from agents.rule_engine import check_rules
from agents.output_agent import create_output
from agents.report_agent import save_report

# Get claim from user (Function Call)
claim = get_claim()

# Validate claim data (Conditional Statement)
if not validate_claim(claim):
    print("Invalid Claim")
    exit()

# Create retrieval query (f-string)
query = f"""
Disease: {claim['disease']}
Hospitalization Days: {claim['days']}
"""

# Retrieve policy evidence from ChromaDB (Function Call)
policy_text = retrieve_policy(query)

print("\n" + "=" * 60)
print("RETRIEVED POLICY EVIDENCE")
print("=" * 60)
print(policy_text[:2000])

# Check rule-based decisions (Function Call)
rule_result = check_rules(claim)

print("\n" + "=" * 60)
print("FINAL DECISION")
print("=" * 60)

# Rule Engine Path
if rule_result:

    print("Decision   :", rule_result["decision"])
    print("Reason     :", rule_result["reason"])
    print("Clause     :", rule_result["clause"])
    print("Confidence :", str(rule_result["confidence"]) + "%")

    json_output = create_output(
        claim["disease"],
        claim["days"],
        rule_result["decision"],
        rule_result["reason"],
        rule_result["clause"],
        rule_result["confidence"]
    )

    print("\nJSON OUTPUT")
    print("-" * 60)
    print(json_output)

    save_report(json_output)

# LLM Path
else:

    result = make_decision(
        claim,
        policy_text
    )

    print("Decision   :", result["decision"])
    print("Reason     :", result["reason"])
    print("Confidence :", str(result["confidence"]) + "%")

    json_output = create_output(
        claim["disease"],
        claim["days"],
        result["decision"],
        result["reason"],
        "LLM Analysis",
        result["confidence"]
    )

    print("\nJSON OUTPUT")
    print("-" * 60)
    print(json_output)

    save_report(json_output)