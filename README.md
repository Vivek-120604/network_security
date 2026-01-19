# Network Security — Phishing Detection

Short description

This project implements a machine learning pipeline to detect phishing (malicious) network entries using scikit-learn. It is organized as a modular training pipeline with components for data ingestion, validation, transformation, model training and evaluation, and a FastAPI-based service for training and prediction.

Highlights

- End-to-end ML pipeline: data ingestion -> validation -> transformation -> model training -> evaluation
- Uses scikit-learn for model training and evaluation
- Provides a FastAPI app with endpoints to trigger training and make predictions
- Stores artifacts and models in local artifact directories (Artifacts/ and saved_models/)

Repository status

- Languages: Python (primary)
- No unit tests detected (recommend adding)
- Contains a hard-coded MongoDB test file (testmonogdb.py) with credentials: remove this from the repo and rotate credentials immediately. Treat this as a security-sensitive artifact.

Prerequisites

- Python 3.9+ (project currently uses base image python:3.10)
- pip
- A MongoDB connection (Atlas or self-hosted) for data ingestion
- Optional: Docker to run the project in a container

Quick start - local

1. Clone the repo

   git clone https://github.com/Vivek-120604/network_security.git
   cd network_security

2. Create a virtual environment and activate it

   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .\.venv\Scripts\activate   # Windows (PowerShell)

3. Install dependencies

   pip install -r requirements.txt

4. Create a .env file at the project root with the following variable (example):

   MongoDB_URL="your_mongodb_connection_string"

   Important: Do NOT commit real credentials. Add .env to .gitignore.

5. Run the API (development)

   python app.py

   By default the app redirects the root (/) to /docs where you can access the interactive API documentation (Swagger UI).

Key endpoints

- GET /train — trigger the pipeline to run end-to-end training (calls TrainingPipeline.run_pipeline())
- POST /predict — accepts a file upload and returns prediction results (see app.py)

Running with Docker

1. Build the image

   docker build -t network_security:latest .

2. Run the container (pass env variable)

   docker run -e MongoDB_URL="your_mongodb_connection_string" -p 8001:8001 network_security:latest

Notes: The Dockerfile uses python:3.10-slim-bullseye and runs app.py directly. Consider using a non-root user, using an ENTRYPOINT with uvicorn for production, and multi-stage builds to minimize image size.

Project structure (high level)

- app.py — FastAPI application with /train and /predict routes
- main.py — script to run the training pipeline programmatically
- networksecurity/ — package containing pipeline components and utilities
  - components/ — data_ingestion.py, data_validation.py, data_transformation.py, model_trainer.py
  - constant/ — training_pipelines constants (paths, names)
  - entity/ — dataclasses for artifacts and config entities
  - exception/ — custom exception class
  - logging/ — logger configuration
  - pipelines/ — TrainingPipeline orchestration
  - utils/ — helper utilities (yaml, object save/load, model evaluation)
- requirements.txt — Python dependencies
- Dockerfile — image build instructions
- setup.py — packaging helper

What I found (issues & recommendations)

- Security: testmonogdb.py contains a MongoDB connection URI with an apparent password. This is a serious security leak — remove the file immediately, revoke/rotate the credentials, and add a .env.example.
- No automated tests. Add unit and integration tests (pytest) for components.
- CI/CD: add GitHub Actions for linting, testing, and build.
- Docker: improve for production (non-root user, smaller image, uvicorn as entrypoint).
- Model persistence: consider versioning saved models and tracking experiments (MLflow).
- Documentation: expand README with examples, expected input format for /predict, and sample outputs.

Suggested next steps

- Remove secrets and sensitive files from repo history (use git filter-repo or BFG)
- Add .env.example and update README with concrete sample values
- Add tests and CI
- Add CONTRIBUTING.md and CODE_OF_CONDUCT if the project is public

---

(README content ends)