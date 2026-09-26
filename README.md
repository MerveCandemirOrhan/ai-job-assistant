# AI Job Assistant

AI-powered job matching application built with Python and Django.

## About the Project

AI Job Assistant helps job seekers understand job postings and compare their CV skills with the technical skills required by a job.

The application uses OpenAI to analyze both job descriptions and CVs, then calculates a match score based on the technical skills found in each.

## Features

* User registration and login
* CV upload
* AI-powered CV skill analysis
* AI-powered job description analysis
* CV-to-job skill matching
* Match score calculation
* Matched and missing skills
* Job search
* Job filtering by location and job type
* Pagination
* User-specific CV access
* Django admin panel

## Technologies

* Python
* Django
* OpenAI API
* SQLite
* HTML
* CSS
* Git

## How It Works

1. A user creates an account.
2. The user uploads a CV.
3. The application extracts the text from the CV.
4. OpenAI analyzes the CV and identifies explicitly mentioned technical skills.
5. Job descriptions are analyzed in the same way.
6. The application compares CV skills with job requirements.
7. A match score is calculated.
8. The user can see matched and missing skills.

## Project Structure

```text
ai-job-assistant/
├── config/
├── jobs/
├── templates/
├── media/
├── job_analyzer.py
├── manage.py
├── requirements.txt
├── README.md
└── test_pdf.py
```

## Installation

Clone the repository and enter the project directory:

```bash
git clone <your-repository-url>
cd ai-job-assistant
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Run database migrations:

```bash
python3 manage.py migrate
```

Start the development server:

```bash
python3 manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/jobs/
```

## Security

Sensitive files such as `.env` and uploaded CV files are excluded from Git using `.gitignore`.

Users can only access their own CVs.

## Future Improvements

Possible future improvements include:

* PostgreSQL support
* Docker
* Cloud deployment
* More advanced semantic CV/job matching
* Job API integration
* Improved user interface
* Automated job recommendations

## Author

Merve Orhan

Computer Engineer | Python & Django Developer
