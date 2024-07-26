import streamlit as st
from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def main():
    st.title("Chat Interface with Document Upload")

    # Chat interface
    st.header("Chat")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Document upload
    st.write("Upload a PDF document to extract its text:")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="file_uploader")

    if uploaded_file is not None:
        with st.spinner('Extracting text from PDF...'):
            text = extract_text_from_pdf(uploaded_file)
            st.success("Text extracted successfully!")
            st.session_state["chat_history"].append({"user": "Bot", "message": "Document content: " + text})

    user_input = st.text_input("You:", key="input")
    if user_input:
        st.session_state["chat_history"].append({"user": "You", "message": user_input})
        st.session_state["chat_history"].append({"user": "Bot", "message": "Processing your message..."})

    for chat in st.session_state["chat_history"]:
        st.write(f"{chat['user']}: {chat['message']}")

if __name__ == "__main__":
    main()
