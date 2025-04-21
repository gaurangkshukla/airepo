PDF Q&A Conversational ChatBot using Artificial intelligence. Hugging Face Model - Transformers using

✅ RAG

✅ FAISS - Vecotr DB

✅ Python

✅ PyPDF2

✅ transformers

✅ Numpy

✅ Streamlit for UI

YouTube: 

Created by Gaurang Shukla

shukla.gaurang@gmail.com

https://www.linkedin.com/in/gaurang-shukla-b809a6143/

Explanation of the Code

    PDF Processing:

        Uses PyPDF2 to extract text from uploaded PDF files

        Splits the text into manageable chunks (500 words each)

    Embedding and Search:

        Uses SentenceTransformer to create embeddings of text chunks

        Uses FAISS (Facebook AI Similarity Search) for efficient similarity search

        Finds the most relevant text chunks for a given question

    Question Answering:

        Uses HuggingFace's question-answering pipeline with the 'deepset/roberta-base-squad2' model

        Processes each relevant chunk to find answers

        Returns the answer with the highest confidence score

    Streamlit UI:

        Simple file uploader for PDFs

        Text input for questions

        Displays the answer, confidence score, and relevant context
