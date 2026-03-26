import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("videos")

def store_text(doc_id, text):
    collection.add(
        documents=[text],
        ids=[doc_id]
    )

def search(query):
    return collection.query(query_texts=[query], n_results=2)