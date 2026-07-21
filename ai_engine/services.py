from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from ai_engine.models import DocumentChunk
from pgvector.django import CosineDistance
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
def extract_pdf_text(file_path):

    loader = PyMuPDFLoader(file_path)

    documents = loader.load()

    return documents
def split_documents(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks=splitter.split_documents(
        documents
    )
    return chunks
def create_embedding_model():
    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings
def generate_embeddings(chunks):

    embedding_model = create_embedding_model()

    texts = []

    for chunk in chunks:
        texts.append(chunk.page_content)

    embeddings = embedding_model.embed_documents(texts)

    return embeddings
def search_similar_chunks(question, document_id, k=5):

    embedding_model = create_embedding_model()

    question_embedding = embedding_model.embed_query(
        question
    )

    results = DocumentChunk.objects.filter(
        document_id=document_id
    ).annotate(
        distance=CosineDistance(
            "embedding",
            question_embedding
        )
    ).order_by(
        "distance"
    )[:k]

    return results
def generate_answer(question, chunks):

    context = "\n\n".join(
        chunk.content for chunk in chunks
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
You are an AI assistant for answering questions from documents.

Use only the provided context.
If the answer is not present in context, say:
"I could not find this information in the document."

Context:
{context}


Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content