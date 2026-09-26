import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from jobs.models import Job
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

client = OpenAI()

# Eski yöntem:
# İş ilanlarında becerileri sabit bir liste üzerinden arıyorduk.
# Artık bu listeyi kullanmıyoruz çünkü becerileri AI çıkarıyor.

# SKILLS = [
#     "Python",
#     "Django",
#     "JavaScript",
#     "React",
#     "SQL",
#     "PostgreSQL",
#     "Git",
#     "AWS",
#     "Docker",
#     "Linux",
# ]


def analyze_job(text):
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Analyze the following job description and identify the technical skills required.

Job description:
{text}

Only include technical skills that are explicitly mentioned
in the job description.

Do not infer, assume, or add skills that are not explicitly mentioned.

Return only the list of technical skills.
"""
    )

    skills = []

    for line in response.output_text.strip().splitlines():
        skill = line.strip().lstrip("-").strip()

        if skill and skill != "[]":
            skills.append(skill)

    return {
        "skills": skills,
        "skill_count": len(skills),
    }

def extract_cv_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def analyze_cv(text):
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Analyze the following CV and identify the technical skills mentioned.

CV:
{text}

Only include technical skills that are explicitly mentioned in the CV.

Technical skills include:
- programming languages
- frameworks and libraries
- databases
- cloud platforms
- operating systems
- development tools
- version control tools
- specific infrastructure and networking technologies

Do not include:
- general concepts
- job responsibilities
- soft skills
- business skills
- generic phrases such as "problem-solving" or "open-source software"

Do not infer, assume, or add skills that are not explicitly mentioned.

Return only the list of technical skills.
"""
    )

    skills = []

    for line in response.output_text.strip().splitlines():
        skill = line.strip().lstrip("-").strip()

        if skill and skill != "[]":
            skills.append(skill)

    return {
        "skills": skills,
        "skill_count": len(skills),
    }

def match_cv_to_job(cv_analysis, job_analysis):
    cv_skills = set(cv_analysis["skills"])
    job_skills = set(job_analysis["skills"])

    matched_skills = cv_skills & job_skills
    missing_skills = job_skills - cv_skills

    if job_skills:
        match_score = round(
            len(matched_skills) / len(job_skills) * 100
        )
    else:
        match_score = 0

    return {
    "match_score": match_score,
    "matched_skills": list(matched_skills),
    "missing_skills": list(missing_skills),
    "total_job_skills": len(job_skills),
}

#Verilen metnin içinde hangi teknik becerilerin bulunduğunu bulmak.    

def main():
    # Django veritabanındaki tüm iş ilanlarını al
    jobs = Job.objects.all()

    for job in jobs:
        text = f"{job.title} {job.company} {job.location} {job.description}"

        result = analyze_job(text)

        print("\nJob:", job.title)
        print("Required skills:")

        for skill in result["skills"]:
            print("-", skill)

        print("Skill count:", result["skill_count"])
        

# Program doğrudan çalıştırıldığında main fonksiyonunu çalıştır
if __name__ == "__main__":
    main()