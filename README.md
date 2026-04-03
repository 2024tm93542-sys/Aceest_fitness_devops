# Minimal Flask DevOps Example

This repository demonstrates a minimal Flask application with DevOps best practices, including CI/CD integration using Jenkins and GitHub Actions. The project features:
- A simple Flask REST API
- SQLite file-based database (initialized via endpoint)
- Unit tests with pytest (in `tests/`)
- Dockerfile for containerization
- Automated pipelines for build and test

---

## Local Development Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the application:**
   ```sh
   python -m app.main
   ```
   The app will start on [http://localhost:5000](http://localhost:5000).
3. **Initialize the database (optional):**
   ```sh
   curl http://localhost:5000/init_db
   ```
4. **Access endpoints:**
   - `/` : Health check (returns Hello, World!)
   - `/init_db` : Initializes the SQLite database

---

## Running Tests Manually

To execute all unit tests using pytest:

```sh
python -m pytest
```

Test files are located in the `tests/` directory. Ensure dependencies are installed before running tests.

---

## Docker Usage

1. **Build the Docker image:**
   ```sh
   docker build -t flask-devops-demo .
   ```
2. **Run the container:**
   ```sh
   docker run -p 5000:5000 flask-devops-demo
   ```

---

## CI/CD Integration Overview

### Jenkins Pipeline
- **Stages:**
  1. Checkout code from SCM
  2. Install Python dependencies
  3. Run unit tests with pytest
  4. Build Docker image
- The pipeline is defined in the `Jenkinsfile` and can be used in a Jenkins server for automated build and test on each commit.

### GitHub Actions Workflow
- **Triggers:** On push or pull request to the `main` branch
- **Steps:**
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies
  4. Run tests with pytest
  5. Build Docker image
- The workflow is defined in `.github/workflows/main.yml` and provides automated CI for every code change on GitHub.

---

## Endpoints
- `/` : Health check (returns Hello, World!)
- `/init_db` : Initializes the SQLite database
