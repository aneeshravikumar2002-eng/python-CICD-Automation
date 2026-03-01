from flask import Flask, render_template_string
from bs4 import BeautifulSoup
import requests
import certifi
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """
    Fetches the title of a webpage and displays it beautifully.
    """
    url = "https://example.com"

    try:
        # ✅ Force requests to use trusted CA bundle
        response = requests.get(
            url,
            timeout=5,
            verify=certifi.where()
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return render_template_string(ERROR_TEMPLATE, error=str(e))

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    return render_template_string(
        HTML_TEMPLATE,
        url=url,
        title=title,
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

# (Rest of your HTML_TEMPLATE and ERROR_TEMPLATE remain EXACTLY SAME)
response = requests.get(url, timeout=5, verify=False)

