# DevSecOps App — Step 1 (Flask + Pytest + Prometheus)

This is **Step 1** of the lab: a minimal Flask API with health checks, an authenticated route, and Prometheus metrics, plus unit tests.

## 1) Create and activate a virtualenv

```bash
cd devsecops-app
python3 -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows PowerShell
# .\venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) (Optional) Configure token

Copy the example env file and set your API token:

```bash
cp .env.example .env
# edit .env and set API_TOKEN=supersecrettoken
```

If no `.env` is provided, the default token is `supersecrettoken`.

## 4) Run the app (development)

```bash
python app.py
# App listens on http://127.0.0.1:5000
```

## 5) Try the routes

- `GET /` → welcome message
- `GET /health` → `{"status":"ok"}`
- `GET /info` → build metadata (version, time, env)
- `GET /secure` (needs token) → send header `X-API-Token: <your_token>` or `?token=<your_token>`
- `GET /metrics` → Prometheus metrics

Example secure call:

```bash
curl -H "X-API-Token: supersecrettoken" http://127.0.0.1:5000/secure
# or
curl "http://127.0.0.1:5000/secure?token=supersecrettoken"
```

## 6) Run tests

```bash
pytest -q
```

---

### Project Tree

```
devsecops-app/
├─ app.py
├─ requirements.txt
├─ .env.example
├─ .gitignore
├─ README.md
└─ tests/
   └─ test_app.py
```
