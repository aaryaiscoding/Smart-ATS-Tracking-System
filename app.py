import streamlit as st
from groq import Groq
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )
    return chat_completion.choices[0].message.content

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
You are an ATS resume evaluator.

Analyze the resume and return the result strictly in the following format:

Score: <number>/100

Strengths:
- point 1
- point 2

Weaknesses:
- point 1
- point 2

Suggestions:
- point 1
- point 2

Keep it concise and structured.
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.warning("Please upload a resume.")

    elif not jd:
        st.warning("Please paste the job description.")

    else:
        st.success("Analyzing resume...")

        text = input_pdf_text(uploaded_file)

        final_prompt = f"""
        {input_prompt}

        Job Description:
        {jd}

        Resume:
        {text}
        """

        response = get_llm_response(final_prompt)

        st.subheader("ATS Analysis")
        st.markdown(response)
