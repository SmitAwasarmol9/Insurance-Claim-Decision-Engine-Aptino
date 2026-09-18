# Insurance Claim Decision Engine

AI-powered Insurance Claim Assessment System using RAG, Rule Engine, FastAPI, Streamlit and LLMs.

## Features

- Policy document retrieval using ChromaDB
- Rule-based claim evaluation
- AI-based decision making using Groq LLM
- Confidence scoring
- Policy clause mapping
- FastAPI REST API
- Streamlit Web Interface
- JSON output generation

## Tech Stack

- Python
- Streamlit
- FastAPI
- ChromaDB
- Sentence Transformers
- Groq LLM
- spaCy

## Workflow

Claim Input
↓
Validation Agent
↓
Policy Retrieval Agent
↓
Rule Engine
↓
LLM Decision Agent
↓
Final Decision Output

## Example Output

```json
{
    "decision": "NOT COVERED",
    "reason": "Asthma treatment not exceeding 3 days is excluded.",
    "clause": "Clause 19 & 20(i)",
    "confidence": 95
}
```

## Run Streamlit

```bash
streamlit run app.py
```

## Run FastAPI

```bash
uvicorn api:app --reload
```