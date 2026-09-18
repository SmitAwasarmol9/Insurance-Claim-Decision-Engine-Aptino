from pypdf import PdfReader

pdf_path = "policy/USGIC-CSCIndividualHealthInsurance_2017-2018.pdf"

reader = PdfReader(pdf_path)

print("Pages:", len(reader.pages))

full_text = ""

for page in reader.pages:
    full_text += page.extract_text() + "\n"

with open("policy_text.txt", "w", encoding="utf-8") as file:
    file.write(full_text)

print("Policy text saved successfully!")