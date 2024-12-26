# import os
import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key not found! Please set it in the environment.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# PDF text extraction
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Text splitting into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

# Generate vector store with embeddings
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Create conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the question as accurately as possible based on the provided context. 
    If the answer is not available in the context, respond with "Answer not available in the context."
    Context: {context}
    Question: {question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", client=genai, temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)

# User input handling
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        #new_db = FAISS.load_local("faiss_index", embeddings)
        new_db = FAISS.load_local(
    "faiss_index", 
    embeddings, 
    allow_dangerous_deserialization=True  
)

    except Exception as e:
        st.error("Error loading vector store. Ensure PDFs are processed first.")
        return {"output_text": ["Error: " + str(e)]}

    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    return chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

# Clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Upload some PDFs and ask me a question."}]

# Main application
def main():
    st.set_page_config(page_title="Gemini PDF Chatbot", page_icon="🤖🤖🖥️")

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("PDFs processed successfully!")
                except Exception as e:
                    st.error(f"Error processing PDFs: {str(e)}")

        st.button("Clear Chat History", on_click=clear_chat_history)

    st.title("Chat with PDF files using Gemini...")
    if "messages" not in st.session_state:
        clear_chat_history()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = user_input(user_prompt)
                if response and "output_text" in response:
                    full_response = "".join(response["output_text"])
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
