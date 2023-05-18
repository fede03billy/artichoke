import requests
import re
from urllib.parse import urlparse
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

    text = soup.get_text()
    # Replace newline and carriage return with space
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # Remove leading/trailing white spaces
    text = text.strip()
    text = re.sub(" +", " ", text)

    main_image = soup.find(
        "img"
    )  # pass {"class": "class-name"} as second argument to find specific image
    image_url = (
        main_image["src"] if main_image else "https://via.placeholder.com/600x300"
    )

    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc
    # check if image url begin with the domain or https (and another domain)
    if not image_url.startswith(domain) and not image_url.startswith("https"):
        image_url = domain + image_url

    scraped_data = {
        "title": soup.title.string,
        "url": url,
        "text": text,
        "image": image_url,
    }

    return jsonify(scraped_data)


if __name__ == "__main__":
    app.run(port=3000)
