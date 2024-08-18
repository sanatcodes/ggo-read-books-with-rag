import streamlit as st
import requests
import json
import os

API_ENDPOINT = "http://localhost:8000"  # Adjust this to your backend URL
DOCUMENT_INFO_FILE = "document_info.json"

def save_document_info(document_id):
    with open(DOCUMENT_INFO_FILE, "w") as f:
        json.dump({"document_id": document_id}, f)

def load_document_info():
    if os.path.exists(DOCUMENT_INFO_FILE):
        with open(DOCUMENT_INFO_FILE, "r") as f:
            return json.load(f).get("document_id")
    return None

def upload_document(file):
    files = {"file": file}
    response = requests.post(f"{API_ENDPOINT}/api/upload_document", files=files)
    if response.status_code == 200:
        document_id = response.json()["document_id"]
        save_document_info(document_id)
        return document_id
    else:
        st.error(f"Error uploading document: {response.text}")
        return None

def get_answer(question, document_id):
    payload = {"question": question, "document_id": document_id}
    response = requests.post(f"{API_ENDPOINT}/api/answer_question", json=payload)
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        st.error(f"Error getting answer: {response.text}")
        return None

def check_document_exists():
    document_id = load_document_info()
    if document_id:
        response = requests.get(f"{API_ENDPOINT}/api/check_document", params={"document_id": document_id})
        if response.status_code == 200:
            return response.json()["exists"]
    return False

def delete_current_document():
    document_id = load_document_info()
    if document_id:
        response = requests.delete(f"{API_ENDPOINT}/api/delete_document", params={"document_id": document_id})
        if response.status_code == 200:
            os.remove(DOCUMENT_INFO_FILE)
            st.success("Document deleted successfully!")
            if "document_id" in st.session_state:
                del st.session_state.document_id
            if "messages" in st.session_state:
                del st.session_state.messages
        else:
            st.error(f"Error deleting document: {response.text}")
    else:
        st.error("No document to delete.")

def main():
    st.set_page_config(layout="wide")
    
    st.title("RAG Chat App")
    st.subheader("Explore Retrieval-Augmented Generation (RAG) with your documents")
    
    st.markdown("""
    This app demonstrates the power of RAG:
    1. Upload a document to create a knowledge base
    2. Ask questions about the content
    3. Get AI-generated answers based on the document
    """)

    document_exists = check_document_exists()

    if not document_exists:
        st.warning("No document uploaded. Please upload a document to start.")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if st.button("Upload Document"):
                with st.spinner("Uploading and processing..."):
                    document_id = upload_document(uploaded_file)
                    if document_id:
                        st.session_state.document_id = document_id
                        st.success("Document uploaded successfully!")
                        st.experimental_rerun()
    else:
        col1, col2 = st.columns([3, 1])
        

        with col2:
            st.header("Document Management")
            st.success("Document loaded and ready for querying!")
            if st.button("Upload New Document"):
                if st.button("Confirm Delete and Upload"):
                    delete_current_document()
                    st.experimental_rerun()
        with col1:
            st.header("Chat Interface")
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("What would you like to know about the document?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing document and generating response..."):
                        document_id = load_document_info()
                        response = get_answer(prompt, document_id)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()