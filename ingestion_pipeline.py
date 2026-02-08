import os
from langchain_community.document_loaders import TextLoader,DirectoryLoader
#to load text files from a directory
from langchain_text_splitters import CharacterTextSplitter
#to split text into smaller chunks
from langchain_voyageai import VoyageAIEmbeddings
#to generate embeddings using Voyage AI
from langchain_chroma import Chroma
#to store and manage embeddings
from dotenv import load_dotenv
#to load environment variables from a .env file

load_dotenv()
# Load environment variables


def load_documents(docs_path="docs"):
    print("Loading documents from:", docs_path)

    if not os.path.exists(docs_path):
        print(f"Directory {docs_path} does not exist.")
        return []
    
    loader = DirectoryLoader(docs_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if len(documents) == 0:
        print(f"No text files found in directory {docs_path}.")

    for i, doc in enumerate(documents[:2]): 
        print(f"Document {i+1}: ")   
        print(f"content length: {len(doc.page_content)} characters")
        print(f"content preview: {doc.page_content[:100]}")  # Print first 500 characters
        print(f"metadata: {doc.metadata}")



    return documents


def split_documents(documents, chunk_size=800, chunk_overlap=0):  
    print("Splitting documents into chunks...")
    
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(documents)
    if chunks: 
        for i, doc in enumerate(chunks[:5]):  
            print(f"Chunk {i+1}: ")
            print(f"length: {len(doc.page_content)} characters")
            print(f"source: {doc.metadata['source']}")  # Print first 500 characters
            print(f"content:")
            print(doc.page_content)  # Print first 100 characters
            print("-" * 40)
    
    if len(chunks) > 5:
        print(f"...and {len(chunks) - 5} more chunks.")
    
    return chunks

def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """Create and persist ChromaDB vector store"""
    print("Creating embeddings and storing in ChromaDB...")
        
    embedding_model = VoyageAIEmbeddings(model="voyage-3", voyage_api_key=os.getenv("VOYAGE_API_KEY"))
    
    # Create ChromaDB vector store
    print("--- Creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("--- Finished creating vector store ---")
    
    print(f"Vector store created and saved to {persist_directory}")
    return vectorstore

def main():
    print ("main function")
    # Step 1: Load Documents
    documents = load_documents(docs_path="docs")
    #step 2: chunk the documents
    chunks = split_documents(documents)
    #step 3: generate embeddings
    vector_store = create_vector_store(chunks)

if __name__ == "__main__":
    main()    