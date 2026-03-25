import re

SKILL_LIST = [
    "python", "java", "c++", "sql", "mysql", "postgresql",
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "opencv", "streamlit", "flask", "fastapi", "docker", "kubernetes",
    "aws", "gcp", "azure", "git", "linux", "data analysis",
    "data visualization", "power bi", "tableau", "transformers",
    "langchain", "faiss", "huggingface", "llm", "rag"
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skills(text: str):
    cleaned = clean_text(text)
    found_skills = set()

    for skill in SKILL_LIST:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cleaned):
            found_skills.add(skill)

    return sorted(found_skills)