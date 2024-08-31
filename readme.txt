# PDF Question Answering App

## Project Background

This project is a Question Answering (QA) system that allows users to upload PDF documents and ask questions about their content. It leverages advanced Natural Language Processing (NLP) techniques and Large Language Models (LLMs) to provide accurate answers based on the document's content.

The system uses a technique called Retrieval-Augmented Generation (RAG), which combines the power of retrieval-based and generative AI methods. Here's how it works:

1. **Document Processing**: When a PDF is uploaded, the system extracts the text and splits it into manageable chunks.

2. **Embedding Generation**: Each chunk is converted into a high-dimensional vector (embedding) that captures its semantic meaning.

3. **Vector Database**: These embeddings are stored in a vector database (Pinecone) for efficient retrieval.

4. **Question Answering**: When a user asks a question, the system:
   - Converts the question into an embedding
   - Retrieves the most relevant document chunks from the vector database
   - Uses a Large Language Model to generate an answer based on the retrieved chunks and the question

This approach allows the system to provide context-aware answers that are grounded in the actual content of the uploaded document, reducing hallucinations and improving accuracy.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:

```
git clone https://github.com/sanatcodes/ggo-read-books-with-rag

```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add the following:

OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
CopyReplace the placeholder values with your actual API keys.

### Running the App

1. Start the backend server:
python -m uvicorn backend.main:app --reload


The backend will be available at `http://localhost:8000`.

2. In a new terminal, start the frontend:
```
streamlit run app.py
```

The frontend will open in your default web browser.

## Using the App

1. Upload a PDF document using the file uploader.
2. Wait for the document to be processed (this may take a few moments depending on the size of the document).
3. Once processing is complete, you can start asking questions about the document in the text input field.
4. The system will provide answers based on the content of the uploaded document.
5. You can upload a new document or clear the chat history at any time using the provided buttons.

## Technical Details

- Backend: FastAPI
- Frontend: Streamlit
- Vector Database: Pinecone
- Language Model: OpenAI's GPT model (via API)
- Embedding Model: Sentence transformers

## Limitations

- The system is designed for text-based PDFs. It may not work well with scanned documents or PDFs with complex layouts.
- The quality of answers depends on the content of the uploaded document and the phrasing of the questions.
- There may be a processing delay for very large documents.

## Future Improvements

- Support for multiple document types (e.g., DOCX, TXT)
- Improved document chunking strategies
- Integration with multiple language models for comparison
- User authentication and document management features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.