import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

# Config
DATA_DIR = "./docs"  # Put your PDFs, .txt, and .md files here
DB_PATH = ".gitlab/agents/chromadb"

def ingest_docs():
    # 1. Load everything from the directory
    # Supports .pdf, .txt, .md automatically via Unstructured
    loader = DirectoryLoader(DATA_DIR, glob="**/*.*", loader_cls=UnstructuredFileLoader)
    documents = loader.load()

    # 2. Split into chunks (Semantic Chunking)
    # Important for PDFs to keep context together
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # 3. Initialize Chroma
    client = chromadb.PersistentClient(path=DB_PATH)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="project_knowledge", embedding_function=ef)

    # 4. Add to DB
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"doc_{i}"],
            documents=[chunk.page_content],
            metadatas=[{
                "source": chunk.metadata.get("source", "unknown"),
                "type": "documentation"
            }]
        )
    print(f"Successfully indexed {len(chunks)} chunks from {len(documents)} files.")

if __name__ == "__main__":
    ingest_docs()
