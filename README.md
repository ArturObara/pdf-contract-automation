# pdf-contract-automation

![Tests](https://github.com/ArturObara/pdf-contract-automation/actions/workflows/tests.yml/badge.svg)

AI-assisted tool that extracts client data from legacy PDF contracts and generates new contracts automatically.

## 1. Overview

This is an internal tool built to automate the generation of new contracts. It automatically extracts client data from legacy PDF documents and dynamically creates new PDF agreements, saving time and eliminating manual data entry for the sales department.

## 2. Key Features

- **PDF Data Extraction:** Extracts data from legacy PDF contracts using Google Gemini API by default for structured field recognition, with native support for PDF form fields (AcroForms) and regex fallback using `pdfplumber` and `pypdf`.
- **Dynamic PDF Generation:** Renders new, print-ready PDF documents from HTML templates using WeasyPrint and Jinja2.
- **REST API:** Built with FastAPI, featuring automatic Swagger documentation and strict data validation with Pydantic schemas.
- **Interactive UI:** A Streamlit dashboard covering the whole flow: upload a legacy PDF, review the extracted data, then generate and download the new contract.
- **Database Management:** PostgreSQL with SQLAlchemy ORM; Alembic migrations are applied automatically on container start.
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

One command starts the database, the API and the dashboard. Database migrations run automatically when the API container starts.

```bash
git clone https://github.com/ArturObara/pdf-contract-automation.git
cd pdf-contract-automation

docker compose up --build
```

That's it. Without a `.env` file the stack uses built-in defaults, and extraction falls back to the regex parser.

To enable Gemini-based extraction or change credentials, create a `.env` first:

```bash
cp .env.example .env
# set GEMINI_API_KEY (and optionally the POSTGRES_* values)
```

## 5. Accessing the App

Once the containers are running:
- **Streamlit Dashboard (UI):** http://localhost:8501
- **FastAPI Docs (Swagger UI):** http://localhost:8000/docs
- **PostgreSQL Database:** localhost:5433 (credentials from `.env`, or the defaults in `docker-compose.yml`)

**Typical workflow (all in the dashboard):**
1. Upload a legacy contract PDF and click **Extract & save client data**. The extracted fields are shown and saved to the database.
2. The contract number is filled in automatically. Click **Generate PDF Contract**.
3. Download the generated upsell contract.

A sample contract to try is in `app/tests/fixtures/test_contract.pdf`.

## 6. Testing

The project includes unit and integration tests. It uses an in-memory SQLite database to test API endpoints and PDF extraction logic in complete isolation.

```bash
# Install dependencies locally (if not already installed)
pip install -r requirements.txt

# Run the test suite
pytest -v
```