import streamlit as st
from utils import analyze_resume, generate_recommendation, get_score_label

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .subtitle {
        font-size: 18px;
        color: #A0A0A0;
        margin-bottom: 24px;
    }
    .box {
        padding: 18px;
        border-radius: 14px;
        background-color: #111827;
        border: 1px solid #2D3748;
        margin-bottom: 16px;
    }
    .metric-card {
        padding: 20px;
        border-radius: 16px;
        background-color: #111827;
        border: 1px solid #2D3748;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

sample_cv = """I am a final-year Artificial Intelligence student with experience in Python, SQL, Machine Learning, Deep Learning, NLP, Pandas, NumPy, Scikit-learn, and Streamlit. I have built projects on resume screening, sentiment analysis, and chatbot systems. Familiar with Git, Linux, and basic Docker."""

sample_jd = """We are looking for an AI Intern Engineer with experience in Python, SQL, Machine Learning, NLP, HuggingFace, LangChain, Docker, AWS, and Git. Candidates with experience deploying AI applications and building NLP systems are preferred."""

with st.sidebar:
    st.header("About This Project")
    st.write("This application compares a candidate resume with a job description using semantic similarity and skill-gap analysis.")
    
    st.subheader("Features")
    st.write("- Resume vs JD matching")
    st.write("- Skill extraction")
    st.write("- Missing skill analysis")
    st.write("- Recommendation generation")

    if st.button("Load Sample Data"):
        st.session_state.cv_text = sample_cv
        st.session_state.jd_text = sample_jd

st.markdown('<div class="main-title">📄 AI Resume Screening System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Compare resumes with job descriptions using NLP, semantic similarity, and skill-gap analysis.</div>',
    unsafe_allow_html=True
)

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    uploaded_cv = st.file_uploader("Upload Resume (.txt)", type=["txt"])
    if uploaded_cv is not None:
        st.session_state.cv_text = uploaded_cv.read().decode("utf-8")

with upload_col2:
    uploaded_jd = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
    if uploaded_jd is not None:
        st.session_state.jd_text = uploaded_jd.read().decode("utf-8")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Candidate Resume")
    cv_text = st.text_area("Paste CV here", value=st.session_state.cv_text, height=320)

with col2:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste Job Description here", value=st.session_state.jd_text, height=320)

analyze_button = st.button("Analyze Match", use_container_width=True)

if analyze_button:
    if not cv_text.strip() or not jd_text.strip():
        st.warning("Please provide both resume text and job description.")
    else:
        result = analyze_resume(cv_text, jd_text)
        recommendation = generate_recommendation(
            result["score"],
            result["missing_skills"],
            result["skill_coverage"]
        )

        score = result["score"]
        coverage = result["skill_coverage"]
        label = get_score_label(score)

        st.divider()
        st.subheader("Analysis Result")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric("Matching Score", f"{score}%")

        with metric2:
            st.metric("Skill Coverage", f"{coverage}%")

        with metric3:
            st.metric("Match Level", label)

        st.progress(min(int(score), 100))

        if score >= 80:
            st.success("This resume is strongly aligned with the job description.")
        elif score >= 60:
            st.warning("This resume is moderately aligned with the job description.")
        else:
            st.error("This resume has a low alignment with the job description.")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### ✅ Matched Skills")
            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.success(skill)
            else:
                st.info("No matched skills found.")

        with col4:
            st.markdown("### ❌ Missing Skills")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.error(skill)
            else:
                st.info("No major missing skills found.")

        st.markdown("### 💡 Recommendation")
        st.info(recommendation)

        extra_col1, extra_col2 = st.columns(2)

        with extra_col1:
            st.markdown("### Resume Skills")
            if result["cv_skills"]:
                st.write(", ".join(result["cv_skills"]))
            else:
                st.write("No skills extracted from resume.")

        with extra_col2:
            st.markdown("### Job Description Skills")
            if result["jd_skills"]:
                st.write(", ".join(result["jd_skills"]))
            else:
                st.write("No skills extracted from job description.")

        if result["extra_skills"]:
            st.markdown("### 🚀 Additional Skills Found in Resume")
            st.write(", ".join(result["extra_skills"]))