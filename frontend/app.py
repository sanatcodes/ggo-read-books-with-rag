import streamlit as st
import requests
import json
import os

API_ENDPOINT = "http://localhost:8000"  # Adjust this to your backend URL

def upload_document(file):
    files = {"file": file}
    response = requests.post(f"{API_ENDPOINT}/api/upload_document", files=files)
    if response.status_code == 200:
        return response.json()["document_id"]
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
    # Placeholder for API call to check if document exists
    # For now, we'll assume it doesn't exist if not in session state
    return "document_id" in st.session_state

def delete_current_document():
    # Placeholder for API call to delete current document
    # For now, we'll just remove it from session state
    if "document_id" in st.session_state:
        del st.session_state.document_id
    if "messages" in st.session_state:
        del st.session_state.messages

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

    st.header("Document Management")
    if not check_document_exists():
        st.warning("No document uploaded. Please upload a document to start.")
        uploaded_file = st.file_uploader("Choose sa PDF file", type="pdf")
        if uploaded_file is not None:
            if st.button("Upload Document"):
                with st.spinner("Uploading and processing..."):
                    document_id = upload_document(uploaded_file)
                    if document_id:
                        st.session_state.document_id = document_id
                        st.success("Document uploaded successfully!")
                        st.experimental_rerun()
    else:
        st.success("Document loaded and ready for querying!")
        if st.button("Upload New Document"):
            if st.popup("Are you sure you want to replace the current document?"):
                delete_current_document()
                st.experimental_rerun()


    st.header("Chat Interface")
    if check_document_exists():
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
                    response = get_answer(prompt, st.session_state.document_id)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.info("Please upload a document to start chatting.")

if __name__ == "__main__":
    main()