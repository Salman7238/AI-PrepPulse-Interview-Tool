import streamlit as st
import google.generativeai as genai
import pdfplumber
import os
from dotenv import load_dotenv
# --- CONFIGURATION ---
load_dotenv() # Load the secret .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Get the key safely

# Configure the AI
genai.configure(api_key=GOOGLE_API_KEY)
# --- FUNCTIONS ---

def extract_text_from_pdf(uploaded_file):
    """Simple function to read text from a PDF file."""
    if uploaded_file is None:
        return None
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        return None
def analyze_readiness(resume_text, job_description):
    """Sends the resume and job description to AI for scoring."""
    
    # This is the "Prompt" - the instructions we give the AI
    prompt = f"""
    You are an expert Technical Interviewer and Career Coach. 
    Review the following Resume against the Job Description.
    
    RESUME TEXT:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Your goal is to assess interview readiness in under 2 minutes.
    
    STRICTLY FOLLOW THIS OUTPUT FORMAT:
    1. **Readiness Score**: (Give a number between 0-100)
    2. **Readiness Level**: (Choose one: Beginner, Intermediate, or Interview-Ready)
    3. **Strengths**: (List 3 bullet points)
    4. **Weaknesses**: (List 3 bullet points of missing skills or weak areas)
    5. **Personalized Improvement Plan**: (Step-by-step guide to fix weaknesses)
    6. **Estimated Timeline**: (Time required to become interview-ready, e.g., "2 weeks")
    
    Be honest, direct, and constructive.
    """
    
    # Get response from Gemini (the AI model)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content(prompt)
    return response.text

# --- THE WEBSITE LAYOUT ---

st.set_page_config(page_title="AI PrepPulse", page_icon="🚀")

st.title("🚀 AI PrepPulse: Interview Readiness Tool")
st.subheader("Build the Future of Interview Readiness")

st.markdown("""
**How it works:**
1. Upload your Resume (PDF).
2. Paste the Job Description you want.
3. Get an instant AI Score & Study Plan!
""")

# Sidebar for inputs
with st.sidebar:
    st.header("📂 User Input")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    job_desc = st.text_area("Paste Job Description Here", height=300)
    analyze_btn = st.button("Analyze Readiness 🚀")

# Main Logic
if analyze_btn:
    if uploaded_file and job_desc:
        with st.spinner("AI is analyzing your profile... (Approx 10 seconds)"):
            # 1. Read PDF
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if resume_text:
                # 2. Ask AI
                result = analyze_readiness(resume_text, job_desc)
                
                # 3. Show Results
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(result)
                
                # 4. Logic Explanation (For Hackathon Judges)
                with st.expander("ℹ️ How was this calculated? (Scoring Logic)"):
                    st.write("""
                    **Scoring Logic:**
                    - **Keyword Matching:** We compared skills in your resume vs. the job description.
                    - **Experience Relevance:** We checked if your past projects align with the role.
                    - **Formatting & Clarity:** Professional structure contributes to the score.
                    - **Gap Analysis:** Missing critical skills lower the readiness level.
                    """)
            else:
                st.error("Could not read the PDF. Please try a standard text-based PDF.")
    else:
        st.warning("Please upload a resume AND paste a job description.")

# Footer
st.markdown("---")
st.caption("Built for AI PrepPulse Hackathon | Made by Salman")
