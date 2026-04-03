# Minimal Flask DevOps Example

This project is a minimal Flask application for DevOps demonstration purposes. It includes:
- A simple Flask API
- SQLite database (file-based, initialized via endpoint)
- Unit tests using pytest (in `tests/`)
- Dockerfile for containerization

## Usage

### Local Development
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app (from the project root):
   ```sh
   python -m app.main
   ```
3. Run tests:
   ```sh
   python -m pytest
   ```

### Docker
1. Build the image:
   ```sh
   docker build -t flask-devops-demo .
   ```
2. Run the container:
   ```sh
   docker run -p 5000:5000 flask-devops-demo
   ```

## Endpoints
- `/` : Health check (returns Hello, World!)
- `/init_db` : Initializes the SQLite database
