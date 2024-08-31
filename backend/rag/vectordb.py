# backend/rag/vectordb.py
from pinecone import Pinecone, ServerlessSpec
from fastapi import HTTPException
import os

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
TOP_K_DOCUMENTS = 3
INDEX_NAME = 'document-indexer'

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists, if not create it
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Get the index
index = pc.Index(INDEX_NAME)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def add_document_to_db(document_id: str, paragraphs: list[str], embeddings: list[list[float]]):
    try:
        vectors = [
            {
                "id": f"{document_id}_{i}",
                "values": embedding,
                "metadata": {"document_id": document_id, "sentence_id": i, "text": paragraph}
            }
            for i, (paragraph, embedding) in enumerate(zip(paragraphs, embeddings))
        ]
        for vector_chunk in chunks(vectors, 100):
            index.upsert(vectors=vector_chunk)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Pinecone indexing failed with error: {e}')

def fetch_top_paragraphs(document_id: str, embedding: list[float]) -> list[str]:
    try:
        query_response = index.query(
            vector=embedding,
            top_k=TOP_K_DOCUMENTS,
            filter={"document_id": {"$eq": document_id}},
            include_metadata=True
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Pinecone query failed with error: {e}')
    
    answers = [match.metadata['text'] for match in query_response['matches']]
    return answers

def document_exists(document_id: str) -> bool:
    try:
        # Fetch a single vector with the given document_id
        response = index.fetch(ids=[f"{document_id}_0"])
        
        # If the response contains any vectors, the document exists
        return len(response['vectors']) > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error checking document existence: {str(e)}')

def delete_document_from_db(document_id: str):
    try:
        # First, we need to fetch all vector IDs associated with this document
        response = index.query(
            vector=[0] * 1024,  # Dummy vector, we're only interested in the metadata
            filter={"document_id": {"$eq": document_id}},
            top_k=10000,  # Adjust this based on your maximum expected paragraphs per document
            include_metadata=False
        )
        
        # Extract the IDs
        vector_ids = [match['id'] for match in response['matches']]
        
        # Delete all vectors associated with this document
        if vector_ids:
            index.delete(ids=vector_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error deleting document: {str(e)}')