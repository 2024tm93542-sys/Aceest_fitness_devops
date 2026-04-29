# 🚀 Minimal Flask DevOps Example

This repository demonstrates a **Flask-based REST API** with complete DevOps lifecycle implementation including:

* CI/CD using **GitHub Actions**
* Containerization using **Docker**
* Deployment on **Azure Kubernetes Service (AKS)**
* Advanced deployment strategies:
  * Rolling Update deployment strategy
  * Canary Deployment (validation in isolated namespace)
  * Blue-Green Deployment (traffic switching via service selector)
  * Automated rollback on failure

---

# 📦 Application Overview

* Flask REST API
* SQLite file-based database
* Pytest unit testing
* Docker containerized application

---

# 🧪 Local Development Setup

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

### 2. Run application

```sh
python -m app.main
```

App runs at:

```
http://localhost:5000
```

### 3. Initialize DB (optional)

```sh
curl http://localhost:5000/init_db
```

---

# 🧪 Running Tests

```sh
python -m pytest
```

Test cases are located in:

```
tests/
```

---

# 🐳 Docker Usage

### Build image

```sh
docker build -t flask-devops-demo .
```

### Run container

```sh
docker run -p 5000:5000 flask-devops-demo
```

---

# ☸️ Kubernetes Deployment (AKS)

This project is deployed on **Azure Kubernetes Service (AKS)** using:

### 🔵 Blue-Green Deployment Strategy

* **Blue = stable production version**
* **Green = new release candidate**
* Traffic is switched via **Service selector update**

### 🟡 Canary Deployment Strategy

* New version deployed in **separate namespace**
* Validated using **port-forward + health checks**
* Cleaned up after validation

### 🔁 Rollback Strategy

* Automatic (triggered on failure) rollback using:

```sh
kubectl rollout undo deployment/flask-app
```

---

# ⚙️ CI/CD Pipeline (GitHub Actions)

### Pipeline stages:

### 1️⃣ Test Stage

* Checkout code
* Setup Python 3.11
* Install dependencies
* Run pytest

### 2️⃣ Build & Push Stage

* Build Docker image
* Tag with:

  * `latest`
  * versioned tag (`vX`)
* Push to Docker Hub

### 3️⃣ Deploy Stage (AKS)

* Deploy Canary in isolated namespace
* Validate via health check
* Deploy Blue-Green resources
* Switch traffic using service selector
* Cleanup canary resources

### 4️⃣ Rollback Stage

* Triggered automatically on failure
* Reverts deployment to previous stable version

## Jenkins Pipeline  
**Stages:** 
1. Checkout code from SCM 
2. Install Python dependencies 
3. Run unit tests with pytest 
4. Build Docker image -  
The pipeline is defined in the Jenkinsfile and can be used in a Jenkins server for automated build and test on each commit.

---

# 🌐 Endpoints

| Endpoint    | Description                |
| ----------- | -------------------------- |
| `/`         | Health check               |
| `/init_db`  | Initialize SQLite database |

---

# 🔄 Deployment Architecture Summary

```
GitHub Push
     ↓
GitHub Actions CI
     ↓
Docker Build + Push
     ↓
AKS Deploy (Canary → Validate)
     ↓
Blue-Green Switch
     ↓
Production Live
     ↓
Rollback (if failure)
```

---

# 🎥 Demo

<video controls src="2024TM93542_DevOps_Assignment_2_demo.mp4" title="Watch Demo"></video>
