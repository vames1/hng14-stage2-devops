# HNG Stage 2 — Containerized Microservices Application

A production-ready containerized job processing system built with Docker, Docker Compose and GitHub Actions CI/CD.

---

## Architecture
| Service | Technology | Port |
|---------|------------|------|
| Frontend | Node.js/Express | 3000 |
| API | Python/FastAPI | 8000 (internal) |
| Worker | Python | - |
| Redis | Redis 7 | 6379 (internal) |

---

## Prerequisites

Make sure you have these installed:

- Docker >= 20.10
- Docker Compose >= 2.0
- Git

---

## Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/vames1/hng14-stage2-devops.git
cd hng14-stage2-devops
```

**2. Create your environment file:**
```bash
cp .env.example .env
```

**3. Update the `.env` file with your values:**
```bash
nano .env
```

**4. Build and start all services:**
```bash
docker-compose up --build -d
```

**5. Verify all services are running:**
```bash
docker-compose ps
```

**6. Access the application:**
---

## What a Successful Startup Looks Like
All services should show **Up** status. The API and frontend should show **(healthy)** after about 30 seconds.

---

## Verifying the Application Works

**Submit a job:**
```bash
curl -X POST http://localhost:3000/submit
```

**Check job status:**
```bash
curl http://localhost:3000/status/{job_id}
```

**Check API health:**
```bash
curl http://localhost:8000/health
```

---

## Stopping the Application

```bash
docker-compose down
```

To also remove volumes:
```bash
docker-compose down -v
```

---

## CI/CD Pipeline

The GitHub Actions pipeline runs these stages in order:

| Stage | What it does |
|-------|-------------|
| **Lint** | Checks Python (flake8), JavaScript (eslint), Dockerfiles (hadolint) |
| **Test** | Runs pytest unit tests with Redis mocked |
| **Build** | Builds and tags all Docker images |
| **Security Scan** | Scans images with Trivy for vulnerabilities |
| **Integration Test** | Brings full stack up and tests end-to-end |
| **Deploy** | Rolling update on pushes to main |

---

## Environment Variables

See `.env.example` for all required variables.

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_PASSWORD` | Redis password | - |
| `API_URL` | API URL for frontend | `http://api:8000` |
| `FRONTEND_PORT` | Frontend port | `3000` |

---

## Author

**Victor Oluwaseyi Akindiose**
Cloud Engineer | Lagos, Nigeria
- Portfolio: https://vames1.github.io
- GitHub: https://github.com/vames1
