# AI Resume Screening System

## Overview

AI Resume Screening System is an NLP-based application that compares a candidate's resume with a job description using semantic similarity and skill-gap analysis.

The system helps users understand how well their profile matches a role by showing:

- Matching score
- Skill coverage
- Matched skills
- Missing skills
- Personalized recommendations

## Demo

### Main Interface

![Demo 1](assets/demo_1.png)

### Analysis Result

![Demo 2](assets/demo_2.png)

## Features

- Semantic similarity with Sentence Transformers
- Rule-based AI/ML skill extraction
- Skill-gap analysis
- Resume and JD text upload
- Interactive Streamlit web interface

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn

## Project Structure

```text
resume-screening-ai/
├── app.py
├── utils.py
├── skill_extractor.py
├── requirements.txt
├── README.md
├── .gitignore
├── sample_data/
│   ├── sample_cv.txt
│   └── sample_jd.txt
└── assets/
    ├── demo_1.png
    └── demo_2.png
```

## Installation

pip install -r requirements.txt

## Run

streamlit run app.py

## Example Use Case

Paste or upload a resume
Paste or upload a job description
Click Analyze Match
Review matching score, skill coverage, matched skills, and recommendations

## Future Improvements

Support PDF and DOCX resume parsing
More advanced skill extraction using spaCy
Job recommendation module
ATS-friendly resume feedback

## Author

Nguyen Trong Tien - 2280603233
