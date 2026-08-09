import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def add_chunks(chunks):

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids
    )


def search(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return "\n".join(results["documents"][0])