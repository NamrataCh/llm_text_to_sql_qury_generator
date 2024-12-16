import PyPDF2
import difflib
import streamlit as st
from html import escape

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to compare two texts and return HTML with highlights
def compare_texts(text1, text2):
    differ = difflib.SequenceMatcher(None, text1, text2)
    result1 = ""
    result2 = ""

    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag == "equal":
            result1 += f'<span style="color: black;">{escape(text1[i1:i2])}</span>'
            result2 += f'<span style="color: black;">{escape(text2[j1:j2])}</span>'
        elif tag == "replace":
            result1 += f'<span style="color: red;">{escape(text1[i1:i2])}</span>'
            result2 += f'<span style="color: green;">{escape(text2[j1:j2])}</span>'
        elif tag == "delete":
            result1 += f'<span style="color: red;">{escape(text1[i1:i2])}</span>'
        elif tag == "insert":
            result2 += f'<span style="color: green;">{escape(text2[j1:j2])}</span>'

    return result1, result2

# Streamlit app
def main():
    st.title("PDF Comparison Tool")

    # File upload
    pdf1 = st.file_uploader("Upload the first PDF", type="pdf")
    pdf2 = st.file_uploader("Upload the second PDF", type="pdf")

    if pdf1 and pdf2:
        with st.spinner("Extracting text from PDFs..."):
            text1 = extract_text_from_pdf(pdf1)
            text2 = extract_text_from_pdf(pdf2)

        with st.spinner("Comparing texts..."):
            html1, html2 = compare_texts(text1, text2)

        st.success("Comparison complete!")

        # Display results
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### First PDF")
            st.markdown(f"<div style='overflow-x: auto;'>{html1}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### Second PDF")
            st.markdown(f"<div style='overflow-x: auto;'>{html2}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
