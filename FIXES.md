# FIXES.md — Bug Documentation

This file documents every bug found in the application, including the file, line number, what the problem was, and how it was fixed.

---

## api/main.py

### Bug 1
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** `host="localhost"` hardcoded — in Docker, services communicate by service name not localhost
- **Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")`

### Bug 2
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** `port=6379` hardcoded — ports should never be hardcoded in production
- **Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))`

### Bug 3
- **File:** `api/main.py`
- **Line:** 6
- **Problem:** No Redis password used — `.env` has `REDIS_PASSWORD` but API ignores it
- **Fix:** Added `password=os.getenv("REDIS_PASSWORD", None)` and `decode_responses=True`

### Bug 4
- **File:** `api/main.py`
- **Line:** 9
- **Problem:** Queue name `"job"` does not match worker which uses `"jobs"` — jobs would never be processed
- **Fix:** Changed `r.lpush("job", job_id)` to `r.lpush("jobs", job_id)`

### Bug 5
- **File:** `api/main.py`
- **Line:** 11
- **Problem:** `status.decode()` called manually — unnecessary and will fail if `decode_responses=True`
- **Fix:** Removed `.decode()` — handled automatically by `decode_responses=True`

### Bug 6
- **File:** `api/main.py`
- **Line:** 13
- **Problem:** Returns `{"error": "not found"}` with HTTP 200 — incorrect HTTP status code
- **Fix:** Replaced with `raise HTTPException(status_code=404, detail="Job not found")`

### Bug 7
- **File:** `api/main.py`
- **Line:** -
- **Problem:** No health check endpoint — Docker cannot verify if the service is healthy
- **Fix:** Added `GET /health` endpoint that pings Redis and returns 503 if unavailable

---

## api/requirements.txt

### Bug 8
- **File:** `api/requirements.txt`
- **Line:** 1-3
- **Problem:** No version pins for `fastapi`, `uvicorn`, `redis` — unpredictable installs in production
- **Fix:** Added pinned versions: `fastapi==0.104.1`, `uvicorn==0.24.0`, `redis==5.0.1`

---

## api/.env

### Bug 9
- **File:** `api/.env`
- **Line:** 1
- **Problem:** `.env` file with real password `supersecretpassword123` committed to repository — critical security vulnerability
- **Fix:** Added `.env` to `.gitignore`, created `.env.example` with placeholder values, removed `.env` from repo

### Bug 10
- **File:** `api/.env`
- **Line:** 1
- **Problem:** `APP_ENV=production` and `REDIS_PASSWORD=supersecretpassword123` on same line — invalid `.env` format
- **Fix:** Each variable on its own line in `.env.example`

---

## worker/worker.py

### Bug 11
- **File:** `worker/worker.py`
- **Line:** 6
- **Problem:** `host="localhost"` hardcoded — worker cannot reach Redis in Docker network
- **Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")`

### Bug 12
- **File:** `worker/worker.py`
- **Line:** 6
- **Problem:** `port=6379` hardcoded — should use environment variable
- **Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))`

### Bug 13
- **File:** `worker/worker.py`
- **Line:** 6
- **Problem:** No Redis password — connection will fail if Redis requires authentication
- **Fix:** Added `password=os.getenv("REDIS_PASSWORD", None)` and `decode_responses=True`

### Bug 14
- **File:** `worker/worker.py`
- **Line:** 4
- **Problem:** `signal` is imported but never used — no graceful shutdown handling
- **Fix:** Implemented proper signal handlers for `SIGTERM` and `SIGINT` to allow graceful shutdown

### Bug 15
- **File:** `worker/worker.py`
- **Line:** 11
- **Problem:** Infinite `while True` loop with no graceful shutdown — bad practice in production containers
- **Fix:** Added `running` flag controlled by signal handlers for clean shutdown

### Bug 16
- **File:** `worker/worker.py`
- **Line:** 7-11
- **Problem:** No error handling — if Redis goes down or job fails the worker crashes silently
- **Fix:** Added try/except blocks with proper logging

---

## worker/requirements.txt

### Bug 17
- **File:** `worker/requirements.txt`
- **Line:** 1
- **Problem:** No version pin for `redis` — unpredictable installs
- **Fix:** Changed to `redis==5.0.1`

### Bug 18
- **File:** `worker/requirements.txt`
- **Line:** -
- **Problem:** Missing `time`, `os`, `signal` are standard library — fine, but no health check dependency
- **Fix:** No change needed for standard library imports

---

## frontend/app.js

### Bug 19
- **File:** `frontend/app.js`
- **Line:** 5
- **Problem:** `API_URL = "http://localhost:8000"` hardcoded — frontend cannot reach API container in Docker
- **Fix:** Changed to `const API_URL = process.env.API_URL || "http://api:8000"`

### Bug 20
- **File:** `frontend/app.js`
- **Line:** 22
- **Problem:** Port `3000` hardcoded — should use environment variable
- **Fix:** Changed to `app.listen(process.env.PORT || 3000)`

### Bug 21
- **File:** `frontend/app.js`
- **Line:** 13, 19
- **Problem:** Vague error message `"something went wrong"` — gives no useful debugging information
- **Fix:** Added proper error logging with `console.error(err.message)`

### Bug 22
- **File:** `frontend/app.js`
- **Line:** 11, 17
- **Problem:** No request timeout on axios calls — if API hangs, frontend hangs forever
- **Fix:** Added `timeout: 5000` to axios config

---

## frontend/package.json

### Bug 23
- **File:** `frontend/package.json`
- **Line:** Last line
- **Problem:** Missing closing `}` — invalid JSON, Node.js will fail to read the file
- **Fix:** Added missing closing `}`

### Bug 24
- **File:** `frontend/package.json`
- **Line:** -
- **Problem:** No `engines` field — Node.js version not specified
- **Fix:** Added `"engines": {"node": ">=18.0.0"}`

### Bug 25
- **File:** `frontend/package.json`
- **Line:** -
- **Problem:** No `package-lock.json` — different versions could install each time
- **Fix:** Generated `package-lock.json` by running `npm install`

---

## frontend/views/index.html

### Bug 26
- **File:** `frontend/views/index.html`
- **Line:** 21
- **Problem:** No error handling in `submitJob()` — if API call fails page shows nothing
- **Fix:** Added try/catch with user-friendly error message display

### Bug 27
- **File:** `frontend/views/index.html`
- **Line:** 27
- **Problem:** No error handling in `pollJob()` — if status check fails polling stops silently
- **Fix:** Added try/catch with retry logic

### Bug 28
- **File:** `frontend/views/index.html`
- **Line:** 31
- **Problem:** No maximum retry limit — if job gets stuck it polls forever
- **Fix:** Added maximum 30 retries (60 seconds) before stopping polling

### Bug 29
- **File:** `frontend/views/index.html`
- **Line:** Last line
- **Problem:** Stray `v` character at end of file
- **Fix:** Removed stray character

---

## Missing Files

### Bug 30
- **File:** `.gitignore`
- **Problem:** No `.gitignore` file — `.env` files and `node_modules` are not excluded
- **Fix:** Created `.gitignore` with proper exclusions

### Bug 31
- **File:** `.env.example`
- **Problem:** No `.env.example` file — developers have no reference for required environment variables
- **Fix:** Created `.env.example` with all required variables and placeholder values

