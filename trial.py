import PyPDF2
import difflib
import streamlit as st
from io import BytesIO

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to compare two texts word by word using difflib
def compare_texts(text1, text2):
    words1 = text1.split()
    words2 = text2.split()
    
    diff = difflib.ndiff(words1, words2)
    
    comparison_result = []
    
    for item in diff:
        if item.startswith(' '):  # Unchanged word
            comparison_result.append(("black", item[2:]))
        elif item.startswith('-'):  # Removed word
            comparison_result.append(("red", item[2:]))
        elif item.startswith('+'):  # Added word
            comparison_result.append(("green", item[2:]))
    
    return comparison_result

# Function to display comparison result with colors
def display_comparison_result(diff_result):
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.header("PDF 1 Text")
        text1 = ""
        for color, word in diff_result:
            if color == "black":
                text1 += f"{word} "
            elif color == "red":
                text1 += f'<span style="color:red">{word}</span> '
            elif color == "green":
                text1 += f'<span style="color:green">{word}</span> '
        st.markdown(text1, unsafe_allow_html=True)
    
    with right_column:
        st.header("PDF 2 Text")
        text2 = ""
        for color, word in diff_result:
            if color == "black":
                text2 += f"{word} "
            elif color == "red":
                text2 += f'<span style="color:red">{word}</span> '
            elif color == "green":
                text2 += f'<span style="color:green">{word}</span> '
        st.markdown(text2, unsafe_allow_html=True)

# Streamlit user interface
def main():
    st.title("PDF Text Comparison with Highlights")
    
    # Upload PDF files
    pdf_file1 = st.file_uploader("Upload the first PDF", type="pdf")
    pdf_file2 = st.file_uploader("Upload the second PDF", type="pdf")
    
    if pdf_file1 and pdf_file2:
        # Extract text from uploaded PDFs
        text1 = extract_text_from_pdf(pdf_file1)
        text2 = extract_text_from_pdf(pdf_file2)
        
        # Compare the texts
        diff_result = compare_texts(text1, text2)
        
        # Display the results side by side with highlights
        display_comparison_result(diff_result)

if __name__ == "__main__":
    main()
