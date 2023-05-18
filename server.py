import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route("/", methods=["POST"])
def scrape_article():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    print(f"Scraping {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    scraped_data = {"title": soup.title.string, "url": url, "text": soup.get_text()}

    return jsonify(scraped_data)


if __name__ == "__main__":
    app.run(port=3000)
