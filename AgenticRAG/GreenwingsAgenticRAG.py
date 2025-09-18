import weaviate
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import gradio as gr

#========== Weaviate Vector DB - FAQ about EV Scooters - code starts ==========


# Configuration
WEAVIATE_URL = "http://localhost:8080"
OLLAMA_HOST = "http://localhost:11434"
DOCUMENTS_DIR = "D:/wspython/Weaviate/docs"
OLLAMA_MODEL = "llama2"


#============= Initialize clients ================
client = weaviate.Client(WEAVIATE_URL)
#ollama = Client(host=OLLAMA_HOST)
print(f"Client is REady = {client.is_ready()}")

# ================ load files from the directory path ======
loader = DirectoryLoader("D:/wspython/AgenticRAG/FAQDocs",glob="**/*.docx")
data = loader.load()
#print(f"{data}")

#================ text splitting =====================
text_splitter  = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap= 20,
    separators=["\n\n", "\n", "? ", ". ", "! "] )
docs = text_splitter.split_documents(data)
#print(f"{docs}")
print(f"Length of doc : {len(docs)}")

#============= Embedding Conversation ================
#embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")



#============= define input structure ==========

#client.schema.delete_all()
#client.schema.delete_class("GreenWingsFAQ")
#client.schema.get()


schema = {
    "classes": [{
        "class": "GreenWingsFAQ",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "source", "dataType": ["string"]}
        ]
    }]
}


#client.schema.create(schema)



with client.batch as batch:
    batch.batch_size = 20  # Smaller batches for reliability
    for i, doc in enumerate(docs):
        try:
            batch.add_data_object(
                data_object={
                    "content": doc.page_content,
                    "source": os.path.basename(doc.metadata["source"])
                },
                class_name="GreenWingsFAQ"
            )
            if i % 10 == 0:  # Print progress
                print(f"Indexed document {i+1}/{len(docs)}")
        except Exception as e:
            print(f"Error indexing doc {i}: {str(e)}")
            print(f"Problematic content: {doc.page_content[:200]}...")

# ====== 3. QUERY FUNCTION ======
def get_answers(question):
    """Get answers with Near Text search"""
    results = client.query.get(
        "GreenWingsFAQ",
        ["content", "source"]
    ).with_near_text({
        "concepts": [question],
        "certainty": 0.45  # Lower threshold
    }).with_limit(3).do()
    
    return results["data"]["Get"]["GreenWingsFAQ"]

# ====== 4. TEST QUERY ======
def get_answer_for_faq_from_weaviate_db(query):
    final_answer=""
    answers = get_answers(query)
    print(f"\nResults for: '{query}'")
    if not answers:
        print("No results found. Try a different query or check your data.")
        final_answer="No Result"
    else:
        for i, answer in enumerate(answers, 1):
            print(f"\nAnswer {i}:")
            print(f"Source: {answer['source']}")
            print(f"Content: {answer['content'][:200]}...")  # First 200 chars
            final_answer += "Weeaviate DB Answer \n"+f"\nAnswer {i}: \n"+f"Source: {answer['source']} \n"+f"Content: {answer['content'][:200]}..."
    
    return final_answer
#========== Weaviate Vector DB - FAQ about EV Scooters - code ends ==========



#========== Chroma Vector DB - Product Manual Docs - code starts ==========
# Configuration
DOCUMENTS_DIR = "D:/wspython/AgenticRAG/ProductManualsDoc"
PERSIST_DIRECTORY = "D:/wspython/AgenticRAG/chroma_db"  # Directory to store ChromaDB

#============= Initialize Vector DB - Chroma DB ================
def initialize_chroma_db(docs):
    # Initialize embedding model
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create ChromaDB
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Persist the DB to disk
    vectordb.persist()
    
    return vectordb

#============= Load Existing Vector DB - Chroma DB ================
def load_existing_chroma_db():
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function
    )
    return vectordb

def query_documents(vectordb, query, k=1):
    results = vectordb.similarity_search(query, k=k)
    return results

def interactive_query(vectordb,query):
    results = query_documents(vectordb, query)
    final_answer = ""
    print(f"\nResults for: '{query}'")    
    #print(f"\nFound {len(results)} relevant documents:")
    for i, doc in enumerate(results, 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content: {doc.page_content[:200]}...")  # Show first 200 chars
        final_answer = "Chroma DB Answer \n"+f"Source: {doc.metadata.get('source', 'Unknown')} \n" + f"Content: {doc.page_content[:200]}..."
    
    return final_answer


def get_answer_for_faq_from_chorma_db(query):
    # Check if we need to create a new DB or load existing
    if not os.path.exists(PERSIST_DIRECTORY):     
        print("Initializing new ChromaDB...")
        loader = DirectoryLoader(DOCUMENTS_DIR, glob="**/*.docx")
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=20,
            separators=["\n\n", "\n", "? ", ". ", "! "]
        )
        docs = text_splitter.split_documents(data)
        print(f"Processed {len(docs)} document chunks")
        
        vectordb = initialize_chroma_db(docs)
    else:
        print("Loading existing ChromaDB...")
        vectordb = load_existing_chroma_db()
    
    # Start interactive query session
    query_to_chromaDB = query
    chromadb_answer = interactive_query(vectordb,query_to_chromaDB)
    return chromadb_answer

#========== Chroma Vector DB - Product Manual Docs - code ends ==========


#========== Context Logic ==========
# --- Agent State and Logic (Unchanged from Original) ---

def classify_query(query):
    get_query = query.lower()
    context = ""
    if any(keyword in get_query for keyword in ["charge", "benefits", "two-wheeler"]):
       context="faq"
    elif any(keyword in get_query for keyword in ["motor", "model", "scooter"]):
        context="manual"
    return context

def retrieve_context(query):
    print(f"query ===> {query}")       
    get_query = query.lower()
    context_type = ""
    if any(keyword in get_query for keyword in ["explain", "benefits", "two-wheeler"]):
       context_type="faq"
    elif any(keyword in get_query for keyword in ["motor", "model", "scooter"]):
        context_type="manual"

    print(f"Context ===> {context_type}")

    retrived_answer = ""
    if context_type == "faq":
         retrived_answer = get_answer_for_faq_from_weaviate_db(query)
    elif context_type == "manual":
        retrived_answer = get_answer_for_faq_from_chorma_db(query)

    return retrived_answer

#asked_query = "explain about GREENWINGS Nova"
#asked_query = "which has BLDC HUB, COATED MOTOR"
asked_query = "which model support a front disc and rear drum brake"
#retrieve_context(asked_query)


title = "✨ Agentic RAG by Gaurang Shukla ✨"
desc = "🎨 If this inspires you, let others know!"
long_desc = "🌟 Enjoyed this? spread the word! "
# Create Gradio Interface
gr.Interface(retrieve_context,"text","text", theme=gr.themes.Glass(),
              title=title, description=desc, article=long_desc).launch(share=True)