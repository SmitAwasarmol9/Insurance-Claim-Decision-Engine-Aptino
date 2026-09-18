# agents/report_agent.py

def save_report(content):

    with open(
        "results/claim_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print("\nReport saved successfully.")