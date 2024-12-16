import streamlit as st
from PyPDF2 import PdfReader
import difflib

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_side_by_side_diff(text1, text2):
    """Generate a side-by-side diff for the two texts."""
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    left_column = []
    right_column = []

    for line in diff:
        if line.startswith("- "):
            left_column.append(f"\033[91m{line[2:]}\033[0m")  # Red for removed text
            right_column.append("")
        elif line.startswith("+ "):
            left_column.append("")
            right_column.append(f"\033[92m{line[2:]}\033[0m")  # Green for added text
        else:
            left_column.append(line[2:])
            right_column.append(line[2:])

    return left_column, right_column

# Streamlit UI
def main():
    st.title("PDF Text Comparison Tool")

    # Upload PDFs
    col1, col2 = st.columns(2)
    with col1:
        pdf1 = st.file_uploader("Upload First PDF", type=["pdf"])
    with col2:
        pdf2 = st.file_uploader("Upload Second PDF", type=["pdf"])

    if pdf1 and pdf2:
        # Extract text from PDFs
        with st.spinner("Extracting text from PDFs..."):
            text1 = extract_text_from_pdf(pdf1)
            text2 = extract_text_from_pdf(pdf2)

        # Generate side-by-side diff
        with st.spinner("Generating comparison..."):
            left_column, right_column = generate_side_by_side_diff(text1, text2)

        # Display the result
        st.subheader("Comparison Results")
        st.markdown("### Side-by-Side Text Comparison ")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text("First PDF")
            st.markdown("<pre style='color: red;'>" + "\n".join(left_column).replace("\033[91m", "<span style='color: red;'>").replace("\033[92m", "<span style='color: green;'>").replace("\033[0m", "</span>") + "</pre>", unsafe_allow_html=True)
        with col2:
            st.text("Second PDF")
            st.markdown("<pre style='color: green;'>" + "\n".join(right_column).replace("\033[91m", "<span style='color: red;'>").replace("\033[92m", "<span style='color: green;'>").replace("\033[0m", "</span>") + "</pre>", unsafe_allow_html=True)
      
if __name__ == "__main__":
    main()
