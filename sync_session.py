import sys
import chromadb
from datetime import datetime

def save_session_to_db(summary):
    client = chromadb.PersistentClient(path=".gitlab/agents/chromadb")
    collection = client.get_or_create_collection(name="session_history")

    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    collection.add(
        ids=[session_id],
        documents=[summary],
        metadatas=[{
            "timestamp": str(datetime.now()),
            "type": "session_memory"
        }]
    )
    return f"Session memory saved with ID: {session_id}"

if __name__ == "__main__":
    summary_input = sys.argv[1] if len(sys.argv) > 1 else ""
    if summary_input:
        print(save_session_to_db(summary_input))
