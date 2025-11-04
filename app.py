import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# ---- App & Config ----
app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
BUILD_TIME = os.getenv("BUILD_TIME") or datetime.now(timezone.utc).isoformat()
ENV_NAME = os.getenv("ENV", "dev")
API_TOKEN = os.getenv("API_TOKEN", "supersecrettoken")

# ---- Prometheus metrics ----
REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total HTTP requests",
    ["endpoint", "method", "status"]
)

def _get_token_from_request(req):
    # Allow header or query parameter
    hdr = req.headers.get("X-API-Token")
    if hdr:
        return hdr.strip()
    return req.args.get("token", "").strip()

@app.after_request
def after_request(response):
    try:
        endpoint = request.endpoint or "unknown"
        REQUEST_COUNT.labels(endpoint=endpoint, method=request.method, status=str(response.status_code)).inc()
    except Exception:
        # Metrics should never break the app
        pass
    return response

# ---- Routes ----
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the DevSecOps Flask API"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/info", methods=["GET"])
def info():
    data = {
        "version": APP_VERSION,
        "build_time": BUILD_TIME,
        "environment": ENV_NAME
    }
    return jsonify(data), 200

@app.route("/secure", methods=["GET"])
def secure():
    token = _get_token_from_request(request)
    if token and token == API_TOKEN:
        return jsonify({"secure": True, "message": "You are authorized"}), 200
    return jsonify({"secure": False, "error": "Unauthorized"}), 401

@app.route("/metrics", methods=["GET"])
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Simple dev server
    app.run(host="127.0.0.1", port=5000, debug=True)
