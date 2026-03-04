from flask import Flask, render_template_string
from bs4 import BeautifulSoup
import requests
import certifi
import logging
import os
from datetime import datetime

app = Flask(__name__)

# ----------------------------
# Configuration
# ----------------------------
TARGET_URL = os.getenv("TARGET_URL", "https://example.com")
REQUEST_TIMEOUT = 5

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ----------------------------
# HTML Templates
# ----------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Website Title Fetcher</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #0f172a;
    color: white;
    text-align: center;
    padding-top: 50px;
}

.card {
    background: #1e293b;
    padding: 30px;
    border-radius: 10px;
    display: inline-block;
}

h1 { color: #38bdf8; }

</style>
</head>

<body>

<div class="card">
<h1>Website Title Fetcher</h1>

<p><strong>URL:</strong> {{url}}</p>
<p><strong>Title:</strong> {{title}}</p>

<p>Checked at: {{timestamp}}</p>

</div>

</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Error</title>
</head>
<body style="font-family:Arial;text-align:center;padding-top:50px">

<h2>⚠ Error Fetching Website</h2>
<p>{{error}}</p>

</body>
</html>
"""

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def index():
    """
    Fetches webpage title and displays it.
    """

    headers = {
        "User-Agent": "DevOps-Title-Fetcher/1.0"
    }

    try:
        response = requests.get(
            TARGET_URL,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            verify=certifi.where()
        )

        response.raise_for_status()

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return render_template_string(ERROR_TEMPLATE, error=str(e))

    soup = BeautifulSoup(response.text, "html.parser")

    title = "No title found"

    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    logging.info(f"Fetched title from {TARGET_URL}")

    return render_template_string(
        HTML_TEMPLATE,
        url=TARGET_URL,
        title=title,
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )


@app.route("/health")
def health():
    """
    Health check endpoint (for Docker / Kubernetes)
    """
    return {"status": "ok"}


# ----------------------------
# Run Application
# ----------------------------

# ----------------------------
# Run Application
# ----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    )
