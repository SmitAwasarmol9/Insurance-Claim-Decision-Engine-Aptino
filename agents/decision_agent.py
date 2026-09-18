from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )

client = Groq(
    api_key=api_key
)

def make_decision(claim, policy_text):

    prompt = f"""
You are an insurance claim evaluation expert.

POLICY EVIDENCE:
{policy_text}

CLAIM DETAILS:
Disease: {claim['disease']}
Hospitalization Days: {claim['days']}

Rules:
1. Use ONLY the policy evidence.
2. Do not assume anything not written in the policy.
3. Return ONLY valid JSON.
4. confidence must be between 0 and 100.

Output Format:

{{
    "decision": "COVERED / NOT COVERED / WAITING PERIOD / NEED MORE INFORMATION",
    "reason": "short explanation",
    "confidence": 85
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    try:
        return json.loads(result)

    except Exception:
        return {
            "decision": "NEED MORE INFORMATION",
            "reason": "Unable to parse LLM response.",
            "confidence": 50
        }