"""Skybyte greeting service."""
from flask import Flask, jsonify, Response
import os
import time
import signal
import sys

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)

VERSION = "1.0.0"
API_TOKEN = os.environ.get("API_TOKEN", "")

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency",
    ["endpoint"]
)

# Graceful shutdown flag
shutting_down = False


def shutdown_handler(signum, frame):
    global shutting_down
    shutting_down = True
    print("Shutting down gracefully...")
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)


@app.route("/")
def hello():
    start = time.time()

    response = jsonify({"message": "Hello, Candidate", "version": VERSION})

    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)

    return response


@app.route("/healthz")
def healthz():
    if shutting_down:
        return "shutting down", 503
    return "ok", 200


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)