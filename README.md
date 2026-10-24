# GuardRail-RAG

### Permission-Aware, Multi-Tenant Retrieval-Augmented Generation

GuardRail-RAG is a document question-answering application built with **FastAPI, PostgreSQL, Qdrant, Google Gemini, and Streamlit**. It combines semantic search with large language models to generate answers grounded in retrieved document context, while applying tenant and role filters during retrieval.

This project explores how authentication, access control, vector search, and LLM-based generation can work together in a multi-tenant RAG system.

## Features

- **User authentication:** Registration and login with Argon2 password hashing.
- **JWT authentication:** Bearer tokens for protected API endpoints.
- **Multi-tenant architecture:** Associate users and document chunks with tenants.
- **Role-aware retrieval:** Filter document retrieval using tenant and role metadata.
- **Semantic search:** Generate embeddings with Sentence Transformers and retrieve relevant chunks from Qdrant.
- **LLM-powered answers:** Generate responses from retrieved context using Google Gemini.
- **Source references:** Include document identifiers and page numbers in the answer context.
- **Interactive interface:** Ask questions through a Streamlit web interface.
- **REST API:** FastAPI endpoints with interactive Swagger documentation.
- **Automated tests:** Pytest tests for authentication, authorization checks, and RAG endpoint behavior.

## Tech Stack

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
| Testing | Pytest, FastAPI TestClient |

## Architecture

```text
                Streamlit UI
                     |
                  HTTP + JWT
                     |
                     v
                  FastAPI
             Authentication
              Authorization
                     |
                     v
                 RAG Service
              Query Embeddings
              Filtered Retrieval
              Context Assembly
              Answer Generation
                     |
            +--------+--------+
            |                 |
            v                 v
          Qdrant           Gemini
       Vector Search    Answer Generation

               PostgreSQL
             Users and Tenants
```

## How It Works

1. A user registers and logs in through the API.
2. FastAPI verifies credentials and issues a JWT access token.
3. The user submits a question through Streamlit.
4. FastAPI validates the token and obtains the user's tenant and role.
5. The RAG service converts the question into an embedding.
6. Qdrant retrieves relevant chunks using tenant and role filters.
7. Retrieved context is passed to Gemini for answer generation.
8. The answer is returned to the interface with source references when available.

## Getting Started

### Prerequisites

- Python compatible with the pinned dependencies in `requirements.txt`
- PostgreSQL
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Naman123-code/GuardRail-RAG.git
cd GuardRail-RAG
```

### 2. Create and activate a virtual environment

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

Create a `.env` file in the project root. Add the variables expected by the application:

```env
DB_USER=your_postgresql_username
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_long_random_secret
```

Replace the placeholders with your own local values. Use a strong, randomly generated JWT secret.

**Never commit your real `.env` file, API keys, database passwords, or JWT secrets to GitHub.**

### 5. Set up PostgreSQL

1. Make sure the PostgreSQL server is running.
2. Create the database specified by `DB_NAME`.
3. Initialize the database tables using the project's database setup code.
4. Ensure a tenant exists before registering users.

### 6. Start the FastAPI backend

From the project root, run:

```powershell
python -m uvicorn app.main:app --reload
```

Useful URLs:

- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

Keep this terminal running.

### 7. Start the Streamlit interface

Open a second terminal in the project root and activate the virtual environment if necessary. Then run:

```powershell
python -m streamlit run app_ui.py
```

Streamlit communicates with FastAPI for authentication and question answering.

## API Endpoints

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

Protected endpoints require a valid bearer token where applicable. See `/docs` for the request and response schemas.

## Testing

Activate the project's virtual environment, navigate to the repository root, and run:

```powershell
python -m pytest tests -v
```

**Latest development result:** 9 tests passed.

The tests cover authentication, authorization checks, and aspects of the question-answering and retrieval workflow. Passing tests do not by themselves establish complete security against every possible cross-tenant data leak.

## Security and Limitations

- Passwords are hashed with Argon2.
- JWTs authenticate requests to protected endpoints.
- Tenant and role metadata are used to filter vector retrieval.
- Authorization must be enforced by the backend, not just the UI.
- Gemini may return errors or become temporarily unavailable due to service limits.
- Generated source references should be checked against the retrieved document chunks.
- This is a portfolio project and has not been independently audited or certified for production security.

## Future Improvements

- More comprehensive cross-tenant leakage tests.
- Validation of generated citations against retrieved chunks.
- Security audit logging.
- More robust handling of LLM errors and timeouts.
- Expanded document management.
- Docker-based deployment and production configuration.

## Author

**Naman Sharma**

Built as a portfolio project exploring secure RAG systems, backend development, vector databases, and LLM-powered applications.
