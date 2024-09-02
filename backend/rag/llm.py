# backend/rag/llm.py
from fastapi import HTTPException
import cohere
import os
import json
import requests

co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

COHERE_EMBEDDING_MODEL = 'embed-english-v3.0'

def fetch_embeddings(texts: list[str], embedding_type: str = 'search_document') -> list[list[float]]:
    try:
        results =  co.embed(
            texts=texts,
            model=COHERE_EMBEDDING_MODEL,
            input_type=embedding_type
        ).embeddings
        return results
    except Exception as e:
        print(e)
        raise HTTPException(404, detail= f'Cohere embedding fetch fail with error {e}')

def question_and_answer_prompt(question: str, context: list[str]) -> str:
    context_str = '\n'.join(context)
    return f"""
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer: 
    """

def synthesize_answer(question: str, context: list[str]) -> str:
    payload = {
        "messages": [
            {
                "role": "assistant",
                "content": "act as an expert question answering system"
            },
            {
                "role": "user",
                "content": question_and_answer_prompt(question, context)
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://giveago-rag.netlify.app/api/llama",
            json=payload
        )

        return response.content
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"