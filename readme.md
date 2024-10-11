# 📚✨ Making Generative Books with RAG: Chat with Your Documents! 🤖💬

## Project Overview 📄

Welcome to **Making Generative Books with RAG**—an app that lets you talk to your books! Upload a PDF, ask questions, and get answers directly from its content. It's like having a conversation with your favorite author! 📖💬
![RAG bot UI](https://github.com/user-attachments/assets/319d8301-3859-42c6-968a-08b9612c1e25)



This app uses **Retrieval-Augmented Generation (RAG)**, a smart blend of retrieval and generative AI. Here's the magic:

1. **Upload a PDF** and the system breaks it into text chunks. 🧩
2. **Embedding Generation**: Transforms text into high-dimensional vectors (embeddings). 📊
3. **Vector Database**: Stores these embeddings in **Pinecone** for quick retrieval. 🗄️
4. **Ask Questions**: The system finds relevant text chunks and uses a **Large Language Model (LLM)** to generate answers. 🎯

---

## Getting Started 🚀

### Prerequisites 🧰

- Python 3.7+ 🐍
- pip 📦

### Installation 🛠️

1. **Clone the repo**:
   ```bash
   git clone https://github.com/sanatcodes/ggo-read-books-with-rag
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**: Create a .env file:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

## Running the App 🏃‍♂️

1. **Start the backend**:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

2. **Start the frontend**:
   ```bash
   streamlit run app.py
   ```

Upload your PDF, ask questions, and get instant answers! 🌟

## Tech Stack 🛠️

- **Backend**: FastAPI 🚀
- **Frontend**: Streamlit 🎨
- **Vector Database**: Pinecone 🗂️
- **Language Model**: Llama 3.1 8B 🦙

## Limitations & Future Improvements 🌱

- Best with text-based PDFs. 🖼️
- Processing time may vary with document size. ⏲️
- Upcoming: Support for DOCX files, improved chunking, and more model options!

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.

Ready to explore the future of interactive reading? Let's dive into **Making Generative Books with RAG**! 📚✨
