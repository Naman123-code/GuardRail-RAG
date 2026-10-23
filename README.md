# 🔐 GuardRail-RAG

### Permission-Aware, Multi-Tenant Retrieval-Augmented Generation

GuardRail-RAG is a document question-answering application built with **FastAPI, PostgreSQL, Qdrant, Google Gemini, and Streamlit**. It combines semantic search with large language models to generate answers grounded in retrieved document context, while applying tenant and role filters during retrieval.

The project explores how authentication, access control, vector search, and LLM-based generation can work together in a multi-tenant RAG system.

## ✨ Features

- **Authentication:** User registration and login with Argon2 password hashing.
- **JWT authorization:** Protect API endpoints using bearer tokens.
- **Multi-tenant architecture:** Associate users and document chunks with tenants.
- **Role-aware retrieval:** Filter document retrieval using tenant and role metadata.
- **Semantic search:** Generate embeddings with Sentence Transformers and retrieve relevant chunks from Qdrant.
- **LLM-powered answers:** Generate responses from retrieved context using Google Gemini.
- **Source references:** Include document identifiers and page numbers in generated answers.
- **Interactive UI:** Ask questions through a Streamlit web interface.
- **REST API:** FastAPI endpoints with interactive Swagger documentation.
- **Automated testing:** Pytest tests for authentication and related functionality.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| Relational database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, Argon2 |
| Vector database | Qdrant |
| Embedding model | Sentence Transformers — `all-MiniLM-L6-v2` |
| LLM | Google Gemini API |
| Testing | Pytest, HTTPX |

## 🏗️ Architecture

```text
                 ┌────────────────────┐
                 │    Streamlit UI    │
                 └─────────┬──────────┘
                           │ HTTP + JWT
                           ▼
                 ┌────────────────────┐
                 │      FastAPI       │
                 │ Authentication     │
                 │ Authorization      │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │     RAG Service    │
                 │ Query Embeddings   │
                 │ Filtered Retrieval │
                 │ Context Assembly   │
                 │ Answer Generation  │
                 └─────────┬──────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
       ┌─────────────────┐   ┌─────────────────┐
       │ Qdrant          │   │ Google Gemini   │
       │ Vector Search   │   │ Answer Creation │
       └─────────────────┘   └─────────────────┘

                 ┌────────────────────┐
                 │    PostgreSQL      │
                 │ Users and Tenants  │
                 └────────────────────┘
```

## 🔄 How It Works

1. A user registers and logs in through the API.
2. FastAPI verifies credentials and issues a JWT access token.
3. The user submits a question through Streamlit.
4. FastAPI validates the token and obtains the user's tenant and role.
5. The RAG service converts the question into an embedding.
6. Qdrant retrieves relevant chunks using tenant and role filters.
7. The retrieved context is passed to Gemini for answer generation.
8. The response is returned to the UI with source references when provided.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or another Python version compatible with the dependencies
- PostgreSQL
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Naman123-code/GuardRail-RAG.git
cd GuardRail-RAG
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Use the variable names expected by your application:

```env
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_long_random_secret
```

Replace the placeholders with your local values. **Never commit your real `.env` file or expose API keys, passwords, or JWT secrets.**

### 5. Set up PostgreSQL

Create the database and initialize the tables using the project's database setup code. Ensure a tenant exists before registering users.

### 6. Start the FastAPI backend

```powershell
python -m uvicorn app.main:app
```

Useful endpoints:

- Health check: `http://127.0.0.1:8000/health`
- API documentation: `http://127.0.0.1:8000/docs`

### 7. Start the Streamlit UI

Open a second terminal in the project root:

```powershell
python -m streamlit run app_ui.py
```

The UI communicates with FastAPI. Authentication, retrieval, and answer generation remain in the backend.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/register` | Register a user |
| POST | `/login` | Log in and obtain a JWT |
| GET | `/me` | Get authenticated user identity |
| GET | `/protected` | Example protected endpoint |
| GET | `/tenant-check/{resource_tenant_id}` | Check tenant access |
| GET | `/admin-only` | Example admin-only endpoint |
| POST | `/ask` | Ask a question about authorized documents |

Protected endpoints require a valid bearer token.

## 🧪 Testing

Run the authentication tests:

```powershell
python -m pytest tests/test_auth.py -v
```

Run all tests:

```powershell
python -m pytest -v
```

The authentication test suite passed seven tests during development. Run the tests on your own checkout to verify the current result.

## 🔒 Security and Limitations

- Passwords are hashed with Argon2.
- JWTs are used to authenticate protected requests.
- Tenant and role metadata are used to filter vector retrieval.
- The backend is responsible for enforcing authorization; the UI is not the security boundary.
- Gemini responses may be unavailable due to API errors or rate limits.
- Generated source references should be verified against the retrieved document chunks.

Tenant-access checks have been exercised during development, but comprehensive end-to-end cross-tenant leakage testing is still needed. This is a portfolio prototype, not a production-certified security system.

## 🛣️ Future Improvements

- Comprehensive cross-tenant retrieval and leakage tests.
- Validation of citations against retrieved chunks.
- Audit logging for security-relevant operations.
- More robust retries and timeouts for LLM requests.
- Document management through the UI.
- Docker-based deployment and production configuration.

## 👨‍💻 Author

**Naman Sharma**

Built as a portfolio project exploring secure RAG systems, backend development, vector databases, and LLM-powered applications.
