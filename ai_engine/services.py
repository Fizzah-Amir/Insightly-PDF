from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from ai_engine.models import DocumentChunk
from pgvector.django import CosineDistance
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import time
load_dotenv()
os.environ["HF_HUB_OFFLINE"] = "1"
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
_embedding_model = None

def create_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding_model
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
def get_llm(model="llama-3.1-8b-instant", temperature=0):
    return ChatGroq(
        model=model,
        temperature=temperature,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        max_retries=0
    )

def generate_answer(question, chunks):

    context = "\n\n".join(
        f"[Page {chunk.page_number}] {chunk.content}"
        for chunk in chunks
    )

    llm = get_llm()

    prompt = f"""
You are an AI assistant for answering questions from documents.

Use only the provided context. Each context block is labeled with its page number.
If the answer is not present in context, say:
"I could not find this information in the document."

Context:
{context}


Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = sorted({
        chunk.page_number
        for chunk in chunks
        if chunk.page_number is not None
    })

    return {
        "answer": response.content,
        "sources": sources
    }




def extract_concepts_for_document(document, pages_per_batch=4):

    chunks = DocumentChunk.objects.filter(
        document=document
    ).order_by("page_number")

    pages = {}
    for chunk in chunks:
        pages.setdefault(chunk.page_number, []).append(chunk.content)

    llm = get_llm()
    extracted = []

    page_numbers = sorted(pages.keys())

    # group pages into batches, e.g. [1,2,3,4], [5,6,7,8], ...
    batches = [
        page_numbers[i:i + pages_per_batch]
        for i in range(0, len(page_numbers), pages_per_batch)
    ]

    for batch in batches:

        batch_text = ""
        for page_number in batch:
            page_content = "\n\n".join(pages[page_number])
            batch_text += f"\n--- Page {page_number} ---\n{page_content}\n"

        prompt = f"""
Extract key concepts/topics for EACH page below.

Rules:
- Return ONLY valid JSON, no extra text, no markdown fences.
- Format: {{"pages": [{{"page_number": 1, "concepts": ["Concept One", "Concept Two"]}}, ...]}}
- List 2 to 5 concepts max per page. Use short noun-phrases, not full sentences.
- If a page has no meaningful concept, return an empty concepts list for it.
- Include an entry for every page shown below, even if empty.

Pages:
{batch_text}
"""

        concept_names_by_page = _call_llm_with_retry(llm, prompt)

        for page_number, concept_names in concept_names_by_page.items():
            for name in concept_names:
                extracted.append({
                    "page_number": page_number,
                    "name": name.strip()
                })
            time.sleep(5)

    return extracted


def _call_llm_with_retry(llm, prompt, max_retries=5):
    """
    Calls the LLM and parses {"pages": [...]}. Retries with increasing
    wait time if Groq's rate limit (429) is hit, instead of failing.
    """

    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)

            raw = response.content.strip()
            raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

            try:
                parsed = json.loads(raw)
            except (json.JSONDecodeError, AttributeError):
                return {}

            result = {}
            for page_entry in parsed.get("pages", []):
                page_number = page_entry.get("page_number")
                result[page_number] = page_entry.get("concepts", [])

            return result

        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10   # 10s, 20s, 30s, 40s...
                time.sleep(wait_time)
                continue
            else:
                raise e

    return {}

def compare_documents(question, document_ids):

    all_chunks = {}
    for doc_id in document_ids:
        all_chunks[doc_id] = search_similar_chunks(question, doc_id)

    context = ""
    for doc_id, chunks in all_chunks.items():
        context += f"\n--- Document {doc_id} ---\n"
        context += "\n".join(
            f"[p.{chunk.page_number}] {chunk.content}"
            for chunk in chunks
        )
        context += "\n"

    llm = get_llm()

    prompt = f"""
You are comparing excerpts from multiple documents to answer a question.

Question:
{question}

Excerpts:
{context}

Compare the excerpts across documents and return ONLY valid JSON, no markdown fences, in this exact format:
{{
  "agreements": ["point where documents agree, mention doc + page"],
  "contradictions": ["point where documents conflict, mention doc + page"],
  "unique_points": {{"Document <id>": ["point only found in this document"]}}
}}

If a category has nothing to report, return an empty list/object for it.
"""

    response = llm.invoke(prompt)

    raw = response.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, AttributeError):
        parsed = {}

    return {
        "agreements": parsed.get("agreements", []),
        "contradictions": parsed.get("contradictions", []),
        "unique_points": parsed.get("unique_points", {}),
    }


def _call_llm_with_retry(llm, prompt, max_retries=5):
    """
    Calls the LLM and parses {"pages": [...]}. Retries with increasing
    wait time if Groq's rate limit (429) is hit, instead of failing.
    """

    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)

            raw = response.content.strip()
            raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

            try:
                parsed = json.loads(raw)
            except (json.JSONDecodeError, AttributeError):
                return {}

            result = {}
            for page_entry in parsed.get("pages", []):
                page_number = page_entry.get("page_number")
                result[page_number] = page_entry.get("concepts", [])

            return result

        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10   # 10s, 20s, 30s, 40s...
                time.sleep(wait_time)
                continue
            else:
                raise e

    return {}

def compare_documents(question, document_ids):

    all_chunks = {}
    for doc_id in document_ids:
        all_chunks[doc_id] = search_similar_chunks(question, doc_id)

    context = ""
    for doc_id, chunks in all_chunks.items():
        context += f"\n--- Document {doc_id} ---\n"
        context += "\n".join(
            f"[p.{chunk.page_number}] {chunk.content}"
            for chunk in chunks
        )
        context += "\n"

    llm = get_llm()

    prompt = f"""
You are comparing excerpts from multiple documents to answer a question.

Question:
{question}

Excerpts:
{context}

Compare the excerpts across documents and return ONLY valid JSON, no markdown fences, in this exact format:
{{
  "agreements": ["point where documents agree, mention doc + page"],
  "contradictions": ["point where documents conflict, mention doc + page"],
  "unique_points": {{"Document <id>": ["point only found in this document"]}}
}}

If a category has nothing to report, return an empty list/object for it.
"""

    response = llm.invoke(prompt)

    raw = response.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, AttributeError):
        parsed = {}

    return {
        "agreements": parsed.get("agreements", []),
        "contradictions": parsed.get("contradictions", []),
        "unique_points": parsed.get("unique_points", {}),
    }