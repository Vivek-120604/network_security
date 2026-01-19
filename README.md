# Network Security — Phishing Detection

A modular Python project that demonstrates an end-to-end machine learning pipeline for detecting phishing/malicious network entries and exposes a minimal HTTP API for running training and making batch predictions.

This README gives safe, high-level instructions for setup, running, and contribution without including any secrets or sensitive information.

---

## Features

- Modular training pipeline: data ingestion → validation → transformation → model training → evaluation
- Training uses scikit-learn models and utilities
- Lightweight HTTP API (FastAPI) with endpoints for:
  - triggering training
  - uploading a CSV and receiving predictions
- Artifacts (models, preprocessors, reports) are saved locally to configurable artifact directories
- Dockerfile included for containerized execution (development-friendly)

---

## Security note 

This repository must never contain plaintext credentials, connection strings, API keys, or other secrets. Always keep secrets out of source control:

- Use a `.env` file (listed in `.gitignore`) or a secrets manager to store credentials.
- Add a `.env.example` with placeholder variables (no real secrets).
- If a secret was accidentally committed, rotate/revoke it immediately and remove it from the repository history (see "Removing secrets from history" below).

Do NOT commit any files containing real credentials. Audit the repository and working tree before pushing.

---

## Prerequisites

- Python 3.9 or newer (project tested with 3.10)
- pip
- Optional: Docker (for containerized runs)
- Optional: MongoDB or other data source if ingestion reads from a database (set connection string via environment variables)

---

## Quickstart (local)

1. Clone the project and change into the directory:

   ```bash
   git clone <your-repo-url>
   cd <project-root>
   ```

2. Create and activate a virtual environment:

   macOS / Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with required variables (example `.env.example` is provided with placeholders). Example variables (placeholders only):

   ```
   # .env (example)
   MONGODB_URL="mongodb+srv://<username>:<password>@<host>/"
   OTHER_SECRET=""
   ```

   - Never paste real credentials into a file you will commit.
   - Add `.env` to `.gitignore`.

5. Run the API (development):

   ```bash
   python app.py
   ```

   or (recommended) run with uvicorn:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8001 --reload
   ```

6. Visit the API docs (Swagger UI) at:

   ```
   http://localhost:8001/docs
   ```

---

## API 

- GET /train
  - Triggers the training pipeline end-to-end.
  - Useful for ad-hoc retraining in development.

- POST /predict
  - Accepts a CSV file upload and returns predictions (or a viewable table).
  - The CSV must follow the same column/features used during training. See "Input data format" below.

The exact endpoint behavior and accepted file schema can be inspected in the API docs at `/docs` when the server is running.

---

## Input data format (predict endpoint)

Provide a CSV with the same feature columns used at training time. If you are not sure which features are required:

- Inspect the training data schema in `Artifacts/` or the data ingestion code to learn expected column names.
- Alternatively, run a small pipeline locally on a known sample dataset to check expected columns.

Example CSV structure (placeholder names — replace with actual feature names used in your project):

```
feature_1,feature_2,feature_3,...
value,value,value,...
```

Do not include target/label column when sending data for prediction unless the endpoint explicitly expects it.

---

## Artifacts and models

- Trained models and preprocessors are saved to configured artifact directories (e.g., `Artifacts/`, `final_model/`, or `saved_models/` depending on config).
- Ensure these directories are writable by the process running training or prediction.

Consider adopting a model registry or experiment tracking (e.g., MLflow) for production-grade workflows and model versioning.

---

## Running with Docker (development)

1. Build the image:

   ```bash
   docker build -t network_security:dev .
   ```

2. Run the container (pass environment variables at runtime — do not bake secrets into the image):

   ```bash
   docker run -e MONGODB_URL="your_connection_string_here" -p 8001:8001 network_security:dev
   ```

Notes:
- For production, run uvicorn with workers and use a process manager/reverse proxy.
- Prefer multi-stage builds and a non-root user for production images.
- Do not store secrets in images.

---

## Logging, tests, and CI

- Add structured logging and rotate logs for long-running services.
- Add automated tests (pytest) for key components:
  - unit tests for utilities (save/load, evaluation)
  - integration tests for data ingestion and model trainer
- Add CI (e.g., GitHub Actions) to run linters, tests, and build images on push.

---

## Removing secrets from history (if needed)

If a credential is accidentally committed, take these steps:

1. Revoke/rotate the leaked credential immediately.
2. Remove the secret from all commits using a history-rewriting tool such as:
   - BFG Repo-Cleaner
   - git-filter-repo

Example (BFG, local use — do not publish credentials anywhere):
```bash
# Example only — DO NOT run with real credentials printed here
bfg --delete-files YOUR_FILE_CONTAINING_SECRET
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

---

## Contributing

Contributions are welcome. Good first steps:

- Open issues for bugs and enhancements.
- Add tests for any new feature or bugfix.
- Follow the repository coding style and add relevant documentation for any change.



