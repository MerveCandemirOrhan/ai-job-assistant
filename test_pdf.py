from pypdf import PdfReader
from job_analyzer import analyze_cv

pdf_path = "media/cvs/merve_orhan.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text() or ""

result = analyze_cv(text)

print("CV Skills:")

for skill in result["skills"]:
    print("-", skill)

print("Skill count:", result["skill_count"])