import requests
import re
import openai
import os
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)


def extract_keywords(text):
    # Define the prompt
    prompt = f"Extract 5 keywords from this text, answer in the form of a comma-separated list: {text}"

    # Make the API request
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Max 4K tokens
            prompt=prompt,
            max_tokens=100,
        )

        # The output will be in the 'choices' field of the response
        keywords = response["choices"][0]["text"].strip()

        # Return the keywords
        return keywords
    except Exception as e:
        if "tokens" in str(e):
            # Exception in case the text is longer than the maximum allowed by the API,
            # Solution would be to split the text into smaller chunks and send them to the API separately
            # For now, we just return an error message
            return "The text is too long to be analysed for keywords."
        else:
            raise e


def summarize_article(text):
    prompt = f"Summarize this text: {text}"

    # Make the API request
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Max 8K tokens
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract the summary from the response
        summary = response["choices"][0]["message"]["content"]

        # Return the summary
        return summary
    except Exception as e:
        if "messages" in str(e):
            # Exception in case the text is longer than the maximum allowed by the API,
            # Solution would be to split the text into smaller chunks and send them to the API separately
            # For now, we just return an error message
            return "The text is too long to be analyzed for summary."
        else:
            raise e


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
        "keywords": extract_keywords(text),
        "summary": summarize_article(text),
    }

    return jsonify(scraped_data)


if __name__ == "__main__":
    app.run(port=3000)
