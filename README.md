# 🧠 Insightly PDF — AI Document Workspace

> **Turn PDFs into interactive, explorable knowledge.**

**Insightly PDF** is an AI-powered document workspace that transforms static PDF documents into interactive learning and research experiences.

Upload a document, ask questions in natural language, receive answers grounded in the original source pages, and visually explore how the document's key concepts connect through an interactive **mind map**.

Built as a **Retrieval-Augmented Generation (RAG)** system with a **Django REST backend** and a **React + TypeScript frontend**.

---

## ✨ Features

### 📄 1. Document Upload & Processing

Upload PDF documents directly through the web application.

After upload, Insightly PDF processes the document through an asynchronous pipeline:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
Vector Indexing
    ↓
Concept Extraction
    ↓
Relationship Extraction
    ↓
Mind Map Generation
    ↓
Document Ready
```

Documents can have different processing states:

* `PROCESSING`
* `READY`
* `FAILED`

The frontend displays the current processing status so users know when their document is ready to explore.

---

### 💬 2. Grounded AI Chat

Users can ask questions about their uploaded documents using natural language.

Instead of relying only on the LLM's general knowledge, Insightly PDF retrieves relevant sections from the uploaded document and provides them as context to the model.

```text
User Question
      ↓
Question Embedding
      ↓
Semantic Retrieval
      ↓
Relevant Document Chunks
      ↓
LLM + Retrieved Context
      ↓
Grounded Answer
```

Example:

> **User:** What are the main causes discussed in Chapter 3?

Insightly PDF searches the uploaded document for the most relevant sections and generates an answer based on the retrieved context.

---

### 📑 3. Page-Level Source Citations

AI-generated answers are connected to their original document sources.

Instead of simply returning:

```text
The answer is X.
```

Insightly PDF can provide:

```text
Answer:
TCP provides reliable communication...

Sources:
📄 Page 42
📄 Page 45
```

This makes responses more **traceable, verifiable, and trustworthy**.

Users can identify where the information came from instead of blindly trusting an AI-generated response.

---

### 🧠 4. AI Concept Extraction

Insightly PDF analyzes processed documents and extracts important concepts.

For example, a Computer Networks document might produce:

```text
TCP
 │
 ├── Reliability
 ├── Flow Control
 ├── Congestion Control
 └── Three-Way Handshake
```

Each concept can be associated with the page where it appears.

These concepts are stored in the backend and later used to construct the interactive mind map.

---

### 🕸️ 5. Interactive Concept Mind Map

One of Insightly PDF's key features is its **interactive document mind map**.

The backend extracts:

* Key concepts
* Concept relationships
* Source pages

The React frontend receives this information and renders it using **React Flow**.

Example:

```text
                 Computer Networks
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
            TCP                     UDP
             │                       │
       ┌─────┴─────┐                 │
       ▼           ▼                 ▼
 Reliability   Flow Control      Low Latency
```

Users can:

* Zoom in and out
* Pan across the graph
* Explore connected concepts
* Understand relationships visually
* Navigate complex topics
* Discover how ideas within the document are connected

This turns a static PDF into an **interactive knowledge graph**.

---

### 📊 6. Document Dashboard

The dashboard provides a central overview of uploaded documents.

Users can view:

* Uploaded documents
* Processing status
* Ready documents
* Pending documents
* Recent activity
* Document statistics

The dashboard gives the application a **workspace-style experience** rather than treating PDFs as isolated files.

---

### 💭 7. Conversation History

Each document can have its own conversation.

Users can:

1. Open a document
2. Start a conversation
3. Ask multiple questions
4. View previous messages
5. Continue the conversation later

Conversation history is stored through the backend and retrieved by the frontend through REST APIs.

---

### 🎯 8. Document-Specific AI

Conversations are associated with specific documents.

When a user asks:

> "Explain this concept."

the system retrieves relevant information from the selected document instead of searching unrelated content.

This keeps the AI interaction focused on the user's actual source material.

---

### 🔎 9. Semantic Search

Insightly PDF uses embeddings to search documents based on **meaning**, not just exact keywords.

For example:

```text
Query:
"How does TCP ensure reliable delivery?"
```

can retrieve content discussing:

```text
Acknowledgements
Packet retransmission
Sequence numbers
Error detection
```

even if the exact phrase "reliable delivery" does not appear in the retrieved text.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ React + TypeScript   │
                         │       Frontend       │
                         └──────────┬───────────┘
                                    │
                              REST / Axios
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Django REST API   │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
              Documents           Chat          Mind Map
                    │               │                │
                    └───────────────┼────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Celery + Redis    │
                         │  Async Processing    │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
          PDF Extraction       Chunking            Embeddings
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ PostgreSQL +         │
                         │ pgvector             │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
                Vector Retrieval          Concept Graph
                       │                         │
                       ▼                         ▼
                      RAG                    React Flow
                       │
                       ▼
                      LLM
                       │
                       ▼
                Grounded Answer
```

---

# 🧠 AI / RAG Architecture

Insightly PDF uses a **Retrieval-Augmented Generation** architecture.

## Document Indexing Pipeline

```text
PDF
 ↓
PyMuPDF
 ↓
Extracted Text
 ↓
Recursive Character Chunking
 ↓
Embedding Model
 ↓
Vector Embeddings
 ↓
PostgreSQL + pgvector
```

Current embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

## Question Answering Pipeline

When a user asks a question:

```text
User Question
      ↓
Generate Query Embedding
      ↓
Vector Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Construct Context
      ↓
LLM
      ↓
Answer + Source Citations
```

The retrieved document chunks provide the factual context for the generated response.

---

# 🕸️ Concept Mind Map Pipeline

The mind map is generated through a separate knowledge-extraction workflow.

```text
Document
    ↓
Processed Text
    ↓
Concept Extraction
    ↓
Relationship Extraction
    ↓
Concepts + Relationships
    ↓
PostgreSQL
    ↓
REST API
    ↓
React Frontend
    ↓
React Flow
    ↓
Interactive Mind Map
```

The backend stores concepts and relationships and exposes them through an API consumed by the frontend.

---

# 🗃️ Core Data Model

## Document

Represents an uploaded PDF.

```text
Document
├── file
├── owner
├── title
├── status
├── mindmap_status
└── timestamps
```

Example document states:

```text
status:
PROCESSING
READY
FAILED
```

Mind map states:

```text
mindmap_status:
NOT_STARTED
PROCESSING
DONE
FAILED
```

---

## Document Chunk

Represents a searchable section of an uploaded document.

```text
Document
   │
   ├── Chunk 1 → Embedding
   ├── Chunk 2 → Embedding
   ├── Chunk 3 → Embedding
   └── Chunk N → Embedding
```

Document chunks are used by the RAG retrieval system.

---

## Concept

Represents an important idea extracted from a document.

```text
Concept
├── document
├── name
├── description
└── page_number
```

The page number allows concepts to be traced back to their original source.

---

## ConceptRelationship

Represents a directed relationship between two concepts.

```text
Concept A
    │
    │ relationship
    ▼
Concept B
```

Example:

```text
TCP
 │
 └── provides → Reliability
```

These relationships are converted into nodes and edges for React Flow.

---

## Conversation

Represents a conversation associated with a document.

```text
Document
   │
   └── Conversation
          │
          ├── User Message
          ├── AI Response
          ├── User Message
          └── AI Response
```

---

# 🛠️ Tech Stack

## Backend

| Technology                | Purpose                              |
| ------------------------- | ------------------------------------ |
| **Python**                | Core backend programming language    |
| **Django**                | Backend web framework                |
| **Django REST Framework** | REST API development                 |
| **PostgreSQL**            | Primary relational database          |
| **pgvector**              | Vector storage and similarity search |
| **Celery**                | Asynchronous task processing         |
| **Redis**                 | Celery message broker                |
| **LangChain**             | Document processing and RAG pipeline |
| **PyMuPDF**               | PDF text extraction                  |
| **Sentence Transformers** | Text embeddings                      |
| **LLM**                   | AI question answering and generation |
| **Docker**                | Containerization                     |
| **Docker Compose**        | Local multi-container development    |

---

## Frontend

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| **React**           | Frontend UI                        |
| **TypeScript**      | Type-safe frontend development     |
| **Vite**            | Frontend build tool                |
| **Tailwind CSS v4** | Styling and UI                     |
| **React Flow**      | Interactive mind map visualization |
| **Axios**           | API communication                  |
| **React Router**    | Client-side routing                |

---

# 🔄 Complete Document Workflow

```text
                    UPLOAD PDF
                        │
                        ▼
                Django REST API
                        │
                        ▼
                 Celery + Redis
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Extract Text          Store File
              │
              ▼
           Chunking
              │
              ▼
         Embeddings
              │
              ▼
     PostgreSQL + pgvector
              │
       ┌──────┴───────┐
       ▼              ▼
   RAG Index      Concept Extraction
       │              │
       │              ▼
       │       Relationships
       │              │
       │              ▼
       │         Mind Map Data
       │              │
       ▼              ▼
     Chat         React Flow
       │              │
       └──────┬───────┘
              ▼
        Interactive
        Document
        Workspace
```

---

# 📡 API Endpoints

The React frontend communicates with Django through REST APIs.

| Method | Endpoint                                          | Purpose                                                 |
| ------ | ------------------------------------------------- | ------------------------------------------------------- |
| `GET`  | `/api/documents/`                                 | List all documents                                      |
| `POST` | `/api/documents/`                                 | Upload a new document                                   |
| `POST` | `/api/documents/chat/start/`                      | Start or resume a document conversation                 |
| `GET`  | `/api/documents/chat/history/<document_id>/`      | Fetch conversation history                              |
| `POST` | `/api/documents/chat/message/`                    | Send a question and receive an AI answer with citations |
| `GET`  | `/api/documents/questions/mindmap/<document_id>/` | Fetch concepts and relationships                        |

> **Note:** Verify the exact paths against the final Django `urls.py` configuration before publishing.

---

# 📁 Project Structure

```text
insightly-pdf/
│
├── backend/
│   │
│   ├── documents/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── tasks.py
│   │   ├── services.py
│   │   └── urls.py
│   │
│   ├── chat/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── celery.py
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── axios.ts
│   │   │
│   │   ├── components/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── DocumentCard.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── StatsCard.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Documents.tsx
│   │   │   ├── Upload.tsx
│   │   │   ├── Chat.tsx
│   │   │   ├── MindMap.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   └── types/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# ⚡ Asynchronous Processing

Document processing can be computationally expensive, especially for large PDFs.

Insightly PDF uses **Celery + Redis** to move heavy workloads into background tasks.

Tasks can include:

* PDF parsing
* Text extraction
* Text chunking
* Embedding generation
* Vector indexing
* Concept extraction
* Relationship generation
* Mind map generation

Instead of blocking the API:

```text
Upload
  ↓
Django API
  ↓
Celery Task
  ↓
Background Processing
  ↓
Database
```

The frontend can then monitor the document's processing status.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/insightly-pdf.git

cd insightly-pdf
```

---

# Backend Setup

## 2. Create Virtual Environment

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=postgres://user:password@localhost:5432/insightly_pdf

REDIS_URL=redis://localhost:6379/0

OPENAI_API_KEY=your_api_key

HF_TOKEN=your_huggingface_token
```

> Replace these values with the environment variables required by your actual backend configuration.

---

## 5. Run Database Migrations

```bash
python manage.py migrate
```

---

## 6. Start Django

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# Celery Setup

Start the Celery worker from the backend directory:

```bash
celery -A <project_name> worker -l info
```

Replace `<project_name>` with your actual Django project package.

---

# Frontend Setup

## 7. Install Dependencies

```bash
cd frontend

npm install
```

---

## 8. Start Development Server

```bash
npm run dev
```

The React application will start through Vite.

The frontend should communicate with the Django API configured in:

```text
src/api/axios.ts
```

---

# 🐳 Docker

Insightly PDF uses Docker for infrastructure and local development.

A typical environment contains:

```text
┌──────────────────┐
│ Django Backend   │
└────────┬─────────┘
         │
         ├──────────────────┐
         ▼                  ▼
┌─────────────────┐  ┌──────────────┐
│ PostgreSQL      │  │    Redis     │
│ + pgvector      │  │              │
└─────────────────┘  └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Celery       │
                     │ Worker       │
                     └──────────────┘
```

Start the infrastructure with:

```bash
docker compose up -d
```

---

# 🔐 Security

Security considerations include:

* Authenticated API access
* User-owned documents
* Permission-protected document endpoints
* File upload validation
* Environment variables for secrets
* Database credentials outside source code
* API keys stored outside the repository

Never commit:

```text
.env
API keys
Database passwords
Secret keys
```

to GitHub.

---

# 📊 Application Flow

A typical user journey:

```text
                 ┌───────────────┐
                 │     Login     │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │   Dashboard   │
                 └───────┬───────┘
                         │
                         ▼
                    Upload PDF
                         │
                         ▼
              ┌────────────────────┐
              │ Background Process │
              └─────────┬──────────┘
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
          RAG Index            Mind Map
              │                    │
              ▼                    ▼
          AI Chat             React Flow
              │                    │
              └─────────┬──────────┘
                        ▼
                Explore Document
```

---

# 🎯 Why Insightly PDF?

Traditional PDF readers allow users to **read** documents.

Insightly PDF allows users to:

```text
READ
 ↓
ASK
 ↓
UNDERSTAND
 ↓
VERIFY
 ↓
EXPLORE
```

A static PDF becomes an interactive knowledge workspace.

### Traditional PDF

```text
PDF
 ↓
Read
```

### Insightly PDF

```text
PDF
 │
 ├── Ask questions
 │
 ├── Get grounded answers
 │
 ├── Verify source pages
 │
 ├── Extract important concepts
 │
 ├── Explore relationships
 │
 └── Visualize knowledge
```

---

# 🌟 What Makes Insightly PDF Different?

The project combines several AI and software engineering concepts into one application:

### 🔹 RAG

Retrieves relevant document context before generating an answer.

### 🔹 Source Citations

Connects AI responses to source pages.

### 🔹 Semantic Search

Retrieves information based on meaning rather than exact keywords.

### 🔹 Knowledge Graph

Represents relationships between important concepts.

### 🔹 React Flow

Turns the extracted knowledge graph into an interactive visual experience.

### 🔹 Async Processing

Celery and Redis handle expensive document-processing tasks in the background.

### 🔹 Full-Stack Architecture

Combines a Django REST API with a modern React frontend.

---

# 🧰 Technologies at a Glance

```text
FRONTEND
├── React
├── TypeScript
├── Vite
├── Tailwind CSS v4
├── React Flow
├── Axios
└── React Router

BACKEND
├── Python
├── Django
├── Django REST Framework
├── Celery
├── Redis
├── LangChain
└── PyMuPDF

AI
├── Retrieval-Augmented Generation
├── Sentence Transformers
├── all-MiniLM-L6-v2
├── Embeddings
├── Semantic Search
├── Vector Retrieval
└── LLM

DATABASE
├── PostgreSQL
└── pgvector

INFRASTRUCTURE
├── Docker
└── Docker Compose
```

---

# 🔮 Roadmap

* [ ] Authentication and multi-user workspaces
* [ ] Multi-document chat
* [ ] Streaming AI responses
* [ ] Document deletion and reprocessing
* [ ] Export mind maps as PNG/PDF
* [ ] Improved RAG retrieval
* [ ] Reranking for better retrieval accuracy
* [ ] Hybrid keyword + vector search
* [ ] Voice-based document interaction
* [ ] Personalized quizzes
* [ ] Learning analytics
* [ ] Multilingual document support
* [ ] Collaborative document workspaces

---

# 🚀 Future Vision

Insightly PDF aims to evolve from an AI-powered PDF assistant into a complete **AI knowledge workspace**.

```text
              DOCUMENT
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
       CHAT    KNOWLEDGE   SUMMARY
                 GRAPH
        │         │         │
        └─────────┼─────────┘
                  ▼
             UNDERSTANDING
                  │
                  ▼
               PRACTICE
                  │
                  ▼
               LEARNING
```

The goal is simple:

> **Don't just read your documents. Understand them, question them, verify them, and see how their ideas connect.**

---

# 📌 Project Highlights

Insightly PDF demonstrates practical experience in:

* Full-stack AI application development
* Django REST API development
* React + TypeScript
* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* Document processing
* LLM integration
* Source-grounded AI
* Page-level citations
* Knowledge graph generation
* React Flow visualization
* PostgreSQL + pgvector
* Celery + Redis
* Docker
* Asynchronous processing
* REST API architecture

---

# 👩‍💻 Project

**Insightly PDF — AI Document Workspace**

> **Upload a document. Ask it anything. See where the answer comes from. Explore how its ideas connect.**
