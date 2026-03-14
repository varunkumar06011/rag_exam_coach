"""
RAG Pipeline — document chunking, embedding, and retrieval
Uses sentence-transformers for embeddings and FAISS for vector search.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5


def build_vectorstore(text: str):
    """
    Split text into chunks, embed them, and build a FAISS vectorstore.
    Returns the vectorstore object.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore


def retrieve_chunks(vectorstore, query: str, k: int = TOP_K) -> str:
    """
    Retrieve top-k relevant chunks from the vectorstore for the given query.
    Returns concatenated chunk text.
    """
    docs = vectorstore.similarity_search(query, k=k)
    combined = "\n\n".join([doc.page_content for doc in docs])
    return combined
