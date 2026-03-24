![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Pytest](https://img.shields.io/badge/Tests-13%20passing-brightgreen)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Argument Analyzer API

A FastAPI service that uses Claude to analyze written arguments and return structured logical components such as the main claim, premises, fallacies, argument strength, and an overall analysis.

This project started as a way to combine my philosophy background with backend development and AI tooling. It has since grown into a more serious API project with authentication, persistence, health checks, request logging, and automated tests.

---

## What It Does

The API accepts a piece of argumentative text, sends it to Claude with a structured prompt, validates the returned JSON, calculates a score, stores the result, and returns a normalized response.

### It currently supports
- User signup and login with bearer-token auth
- Argument analysis through a protected API endpoint
- Persistent storage of analyses in the database
- Health and DB-readiness endpoints
- Request logging middleware
- Automated tests for health, auth, and core analysis behavior

---

## Example

### Request

```bash
curl -X POST "http://127.0.0.1:8000/arguments/analyze" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "text": "God exists because the Bible says so, and the Bible is true because it is the word of God."
  }'
```

### Example Response

```json
{
  "id": 1,
  "text": "God exists because the Bible says so, and the Bible is true because it is the word of God.",
  "main_claim": "God exists",
  "premises": [
    {
      "text": "The Bible says God exists",
      "type": "supporting",
      "order": 0
    },
    {
      "text": "The Bible is true because it is the word of God",
      "type": "supporting",
      "order": 1
    }
  ],
  "fallacies": [
    {
      "type": "circular reasoning",
      "explanation": "The argument assumes the truth of its own source in order to justify the conclusion.",
      "confidence": 0.91
    }
  ],
  "argument_strength": "weak",
  "analysis": "The reasoning is circular because the truth of the Bible is justified by the claim that it is the word of God, which depends on the very conclusion being argued for.",
  "score": 35
}
```

---

## Tech Stack

- **FastAPI** — API framework
- **Anthropic Claude** — LLM used for argument analysis
- **SQLAlchemy** — ORM and database layer
- **PostgreSQL / SQLite** — persistence
- **Docker / Docker Compose** — local containerized setup
- **Pytest** — automated testing

---

## Project Structure

```text
argument-analyzer-v2/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── services/
├── prompts.py
├── utils.py
├── tests/
├── docker-compose.yml
└── requirements.txt
```

### Architecture Overview

- **routers/** defines the API endpoints
- **services/** handles auth logic and Claude integration
- **models/** defines database tables
- **schemas/** defines request/response shapes
- **db.py** configures the database engine and session handling
- **utils.py** handles JSON extraction, validation, and scoring
- **tests/** verifies health, auth, and argument-analysis flows

---

## API Endpoints

### Health
- `GET /` — basic root response
- `GET /health` — service liveness check
- `GET /health/db` — database readiness check

### Auth
- `POST /auth/signup` — create a user and return a token
- `POST /auth/login` — authenticate and return a token
- `GET /auth/me` — return the current authenticated user

### Arguments
- `POST /arguments/analyze` — analyze a new argument
- `GET /arguments` — list saved analyses for the current user

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/stellancathcart/argument-analyzer-v2.git
cd argument-analyzer-v2
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./argument_db.sqlite3
SECRET_KEY=change-me
ANTHROPIC_API_KEY=your_key_here
ACCESS_TOKEN_EXPIRE_HOURS=24
```

### 5. Run the app

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## Docker Setup

To run the app and database with Docker Compose:

```bash
docker compose up --build
```

---

## Testing

Run the test suite with:

```bash
python -m pytest
```

Current tests cover:
- Health and DB-readiness endpoints
- Signup and login flows
- Duplicate signup rejection
- Protected-route behavior
- Argument analysis with mocked Claude responses
- Failure behavior when the external analysis layer breaks

---

## Why I Built It

I’m a philosophy student interested in reasoning, argument structure, AI systems, and backend development. This project began as a way to explore those interests together: using LLMs not just for open-ended generation, but for structured analysis with validation, persistence, and API design around it.

It also serves as a foundation for growing toward more serious AI-platform / backend / MLOps-style work.

---

## Current Strengths

- Structured API design
- Authenticated user flows
- Database-backed persistence
- Request logging and health checks
- Automated backend testing
- Clear separation between routing, services, models, and schemas

---

## Next Steps

- Return and store more analysis metadata such as:
  - Model name
  - Prompt version
  - Latency
  - Analysis status
  - Error type
- Improve production deployment
- Add richer failure handling around external model calls
- Expand test coverage further
- Add a lightweight frontend or demo layer for usability
- Explore evaluation and observability features for AI analysis workflows

---

## License

MIT
