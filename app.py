import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


def gemini_response(resume_text, jd_text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Hey Act Like a skilled or very experienced ATS (Application Tracking System)
    with a deep understanding of tech fields, software engineering, data science, data analysis,
    and big data engineering. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive, and you should provide 
    the best assistance for improving the resumes. Assign the percentage matching based 
    on JD and the missing keywords with high accuracy.
    resume:{{resume_text}}
    description:{{jd_text}}

    I want the response in dictionary format having the structure
    {{"JD Match":"%",
    "MissingKeywords":[],
    "Profile Summary":""}}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit App
st.title("SMART ATS")

st.header("Improve Your Resume with SMART ATS")

st.markdown("""
    <style>
      body {
            font-family: 'Arial', sans-serif;

            background: url('https://source.unsplash.com/light-bulb-on-pile-of-books-qYxIVsHpDDo') no-repeat center center fixed; 
            -webkit-background-size: cover;
            -moz-background-size: cover;
            -o-background-size: cover;
            background-size: cover; 
        }
        
        .text-container {
            margin-bottom: 20px;
        }
        
         .result-block {
            margin-bottom: 20px;
        }
        
        .block-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)

# Job Description Input
jd = st.text_area("Paste Job Description", height=200)
st.markdown("<div class='textarea-container'></div>", unsafe_allow_html=True)

# Resume Upload
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Submit Button
submit_button = st.button("Submit")

if submit_button:
    if file is not None and jd:
        resume_text = input_pdf_text(uploaded_file=file)
        final_response = gemini_response(resume_text, jd)

        # Parse the response into a dictionary
        response_dict = eval(final_response) if final_response else {}

        # st.markdown("<div class='result-container'>", unsafe_allow_html=True)

        # JD Match Block
        if "JD Match" in response_dict:
            st.markdown("<div class='result-block'>", unsafe_allow_html=True)
            st.markdown("<div class='block-title'>JD Match</div>", unsafe_allow_html=True)
            st.write(response_dict["JD Match"])
            st.markdown("</div>", unsafe_allow_html=True)

        # Missing Keywords Block
        if "MissingKeywords" in response_dict:
            st.markdown("<div class='result-block'>", unsafe_allow_html=True)
            st.markdown("<div class='block-title'>Missing Keywords</div>", unsafe_allow_html=True)
            st.write(response_dict["MissingKeywords"])
            st.markdown("</div>", unsafe_allow_html=True)

        # Profile Summary Block
        if "Profile Summary" in response_dict:
            st.markdown("<div class='result-block'>", unsafe_allow_html=True)
            st.markdown("<div class='block-title'>Profile Summary</div>", unsafe_allow_html=True)
            st.write(response_dict["Profile Summary"])
            st.markdown("</div>", unsafe_allow_html=True)