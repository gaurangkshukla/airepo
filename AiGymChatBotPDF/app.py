import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

## Created by Gaurang Shukla

## Initialize models
st.set_page_config(layout="wide")

@st.cache_resource
def load_qa_model():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

qa_pipeline = load_qa_model()
embedder = load_embedding_model()

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def create_faiss_index(text_chunks, embedder):
    embeddings = embedder.encode(text_chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings

def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def find_relevant_chunks(question, index, text_chunks, embedder, top_k=3):
    question_embedding = embedder.encode([question])
    distances, indices = index.search(question_embedding, top_k)
    relevant_chunks = [text_chunks[i] for i in indices[0]]
    return relevant_chunks

def answer_question(question, relevant_chunks, qa_pipeline):
    answers = []
    for chunk in relevant_chunks:
        answer = qa_pipeline(question=question, context=chunk)
        answers.append(answer)
    # Sort answers by score and return the best one
    best_answer = sorted(answers, key=lambda x: x['score'], reverse=True)[0]
    return best_answer

def main():
    st.title("PDF Q&ABot - RAG by Gaurang Shukla")

    
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text
        text = extract_text_from_pdf(uploaded_file)
        
        # Split text into chunks
        text_chunks = split_text_into_chunks(text)
        
        # Create FAISS index
        index, _ = create_faiss_index(text_chunks, embedder)
        
        # Question input
        question = st.text_input("Ask a question about the document:")
        
        if question:
            # Find relevant chunks
            relevant_chunks = find_relevant_chunks(question, index, text_chunks, embedder)
            
            # Get answer
            answer = answer_question(question, relevant_chunks, qa_pipeline)
            
            # Display results
            st.subheader("Answer:")
            st.write(answer['answer'])
            
            st.subheader("Confidence Score:")
            st.write(f"{answer['score']:.2f}")
            
            st.subheader("Relevant Context:")
            for i, chunk in enumerate(relevant_chunks, 1):
                st.write(f"**Chunk {i}:**")
                st.write(chunk[:500] + "...")  # Show first 500 chars of each chunk

if __name__ == "__main__":
    main()