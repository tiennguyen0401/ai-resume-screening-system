from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import extract_skills

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(cv_text: str, jd_text: str) -> float:
    cv_embedding = model.encode(cv_text)
    jd_embedding = model.encode(jd_text)

    score = cosine_similarity([cv_embedding], [jd_embedding])[0][0]
    return max(0.0, float(score))

def analyze_resume(cv_text: str, jd_text: str):
    similarity_score = compute_similarity(cv_text, jd_text)

    cv_skills = set(extract_skills(cv_text))
    jd_skills = set(extract_skills(jd_text))

    matched_skills = sorted(cv_skills.intersection(jd_skills))
    missing_skills = sorted(jd_skills - cv_skills)
    extra_skills = sorted(cv_skills - jd_skills)

    skill_coverage = 0.0
    if len(jd_skills) > 0:
        skill_coverage = len(matched_skills) / len(jd_skills) * 100

    return {
        "score": round(similarity_score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "cv_skills": sorted(cv_skills),
        "jd_skills": sorted(jd_skills),
        "skill_coverage": round(skill_coverage, 2),
    }

def get_score_label(score: float) -> str:
    if score >= 80:
        return "Strong Match"
    elif score >= 60:
        return "Moderate Match"
    else:
        return "Low Match"

def generate_recommendation(score: float, missing_skills: list, coverage: float) -> str:
    if score >= 80 and coverage >= 70:
        return (
            "Your resume is well aligned with this job description. "
            "You already match many of the key requirements. "
            "Focus on presenting project impact, deployment experience, and measurable results more clearly."
        )
    elif score >= 60:
        if missing_skills:
            return (
                "Your profile shows partial alignment with the role. "
                f"Consider strengthening the following skills: {', '.join(missing_skills[:5])}. "
                "You should also tailor your project descriptions to better reflect the job requirements."
            )
        return (
            "Your profile has a moderate match. "
            "Try rewriting your resume using stronger AI/ML keywords and clearer project outcomes."
        )
    else:
        if missing_skills:
            return (
                "Your resume is currently not strongly aligned with this role. "
                f"Important missing skills include: {', '.join(missing_skills[:5])}. "
                "You should revise your resume and add more relevant AI/ML or deployment-related experience."
            )
        return (
            "Your resume is not strongly aligned with the role yet. "
            "Try adding more relevant technical experience, tools, and project details."
        )