# pdf-contract-automation

![Tests](https://github.com/ArturObara/pdf-contract-automation/actions/workflows/tests.yml/badge.svg)

AI-assisted tool that extracts client data from legacy PDF contracts and generates new contracts automatically.

## 1. Overview

This is an internal tool built to automate the generation of new contracts. It automatically extracts client data from legacy PDF documents and dynamically creates new PDF agreements, saving time and eliminating manual data entry for the sales department.

## 2. Key Features

- **PDF Data Extraction:** Extracts data from legacy PDF contracts using Google Gemini API by default for structured field recognition, with native support for PDF form fields (AcroForms) and regex fallback using `pdfplumber` and `pypdf`.
- **Dynamic PDF Generation:** Renders new, print-ready PDF documents from HTML templates using WeasyPrint and Jinja2.
- **REST API:** Built with FastAPI, featuring automatic Swagger documentation and strict data validation with Pydantic schemas.
- **Interactive UI:** A lightweight Streamlit dashboard allowing users to quickly generate and download new contracts.
- **Database Management:** PostgreSQL with SQLAlchemy ORM and Alembic for automated database migrations.
- **Fully Dockerized:** Containerized setup for the database, API, and frontend ensures a consistent local development environment.

## 3. Tech Stack

- **Language:** Python 3.12
- **AI / LLM:** Google Gemini API (`google-genai`)
- **Frameworks:** FastAPI, Streamlit
- **Database:** PostgreSQL 16, SQLAlchemy, Alembic
- **PDF Processing:** WeasyPrint, Jinja2, pdfplumber, pypdf
- **Infrastructure:** Docker, Docker Compose
- **Testing:** Pytest, HTTPX

## 4. Quick Start / Setup

Follow these steps to run the project locally using Docker.

```bash
# 1. Clone the repository
git clone https://github.com/ArturObara/pdf-contract-automation.git
cd pdf-contract-automation

# 2. Set up environment variables
cp .env.example .env
# Note: Ensure POSTGRES_PORT=5433 and GEMINI_API_KEY are set in your .env file.

# 3. Spin up the containers
docker-compose up -d --build

# 4. Run Database Migrations (inside the API container)
docker exec -it pv_fastapi_app alembic upgrade head
```

## 5. Accessing the App

Once the containers are successfully running, the system is available at:
- **Streamlit Dashboard (UI):** http://localhost:8501
- **FastAPI Docs (Swagger UI):** http://localhost:8000/docs
- **PostgreSQL Database:** localhost:5433 (accessible with DB clients like DBeaver using credentials from `.env`)

Contracts are uploaded via Swagger UI (`POST /contracts/upload`). The Streamlit dashboard is used to generate a new upsell contract from an existing record.

**Typical workflow:**
1. Upload a legacy contract PDF via Swagger UI (`POST /contracts/upload`).
2. Open the Streamlit dashboard and enter the old contract number.
3. Download the generated upsell contract.

## 6. Testing

The project includes unit and integration tests. It uses an in-memory SQLite database to test API endpoints and PDF extraction logic in complete isolation.

```bash
# Install dependencies locally (if not already installed)
pip install -r requirements.txt

# Run the test suite
pytest -v
```