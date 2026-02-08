# rag-bot-using-voyage-api

A minimal retrieval-augmented generation (RAG) pipeline that ingests plain-text documents, splits them into chunks, creates embeddings, and stores them in a ChromaDB vector store for later retrieval.

**Files**
- `ingestion_pipeline.py`: Loads `docs/` text files, chunks them, creates embeddings, and saves a ChromaDB vector store.
- `retrieval_pipeline.py`: (placeholder) Use this to implement query/retrieval + generation flows.
- `docs/`: Place one or more `.txt` documents here (examples included).

**Requirements**
- Python 3.9+ (tested with 3.9)
- A virtual environment (recommended)

**Install**
- Create & activate a venv (macOS / Linux):

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
# or if you don't have requirements.txt
pip install langchain-community langchain-chroma langchain-voyageai langchain-openai langchain-text-splitters chromadb python-dotenv
```

**Environment variables**
Create a `.env` file in the project root with one of the following keys:

- For Voyage AI (recommended free model):

```
VOYAGE_API_KEY=your_voyage_api_key_here
```

- For OpenAI (if you prefer OpenAI embeddings):

```
OPENAI_API_KEY=your_openai_api_key_here
```

The pipeline detects the embedding class in the code; edit `ingestion_pipeline.py` to switch providers if needed.

**Run the ingestion pipeline**

```bash
python ingestion_pipeline.py
```

This will:
- Load text files from `docs/`
- Split them into chunks
- Create embeddings and persist a ChromaDB store in `db/chroma_db`

**Rate limits & batching**
- Hosted providers often apply rate limits. If you hit rate-limit errors, you can:
  - Add a brief delay and batch the embedding requests in `ingestion_pipeline.py`.
  - Reduce `chunk_size` or increase `batch_size`/delay between batches.
- Voyage AI: free tokens are available, but adding a payment method increases rate limits.
- OpenAI: may require billing for higher usage.

**Troubleshooting**
- ModuleNotFoundError: install missing packages and ensure venv is activated.
- RateLimitError / insufficient_quota: switch provider, add billing, or process smaller batches with delays.
- If embeddings fail, ensure the correct API key is set in `.env` and `load_dotenv()` is called in the pipeline.

**Next steps / suggestions**
- Implement `retrieval_pipeline.py` to run similarity search against the saved ChromaDB and produce model answers.
- Add a `requirements.txt` by running `pip freeze > requirements.txt` after installing packages.
- Add unit tests for chunking and embedding logic.

**Contact**
- For help, run the ingestion script and paste the error output into the issue or chat.

---

Created by: Project workspace at root (ingestion_pipeline.py, retrieval_pipeline.py, docs/)
