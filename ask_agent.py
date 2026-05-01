import os
import chromadb
from chromadb.utils import embedding_functions

# Local vs. CI Path Resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "../../.gitlab/agents/chromadb")
PROJECT_ID = os.getenv("PROJECT_IDENTIFIER", "local-dev-repo")

def query_memory(question):
    # Use a persistent client to access the local vector store
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Must match the model used in train_memory.py
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    try:
        collection = client.get_collection(name="terraform_knowledge", embedding_function=ef)
        
        # Pass the plain text string; the library handles the vector conversion
        results = collection.query(
            query_texts=[question],
            n_results=2,
            where={"project_id": PROJECT_ID}
        )

        if not results['documents'][0]:
            return "No specific infrastructure standards found in memory."

        output = "### Relevant Project Standards Found:\n"
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            output += f"- **Source**: {meta.get('name', 'General')}\n- **Guidance**: {doc[:500]}\n\n"
        return output
    except Exception as e:
        return f"Error accessing memory: {str(e)}"

if __name__ == "__main__":
    import sys
    query_text = " ".join(sys.argv[1:])
    if query_text:
        print(query_memory(query_text))
