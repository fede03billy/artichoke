# Artichoke
The code in this repo allows you to extract info about an article from its URL.
The info are the following:
- The URL you are scraping
- Title of the article
- First image in the webpage (the `src` URL)
- 5 keywords (in a comma-separated list) (max article lenght to use this feature: 4000 words)
- A summary of the text (max article lenght to use this feature: 6600 words)
- All the text and only the text found in the page as a string

## Requirements
To use this program, you need to have the following installed:
- Python 3
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)
- OpenAI library (`pip install openai`)

## Usage
### In another project
You can import the main function as follow:
```
from artichoke import scrape_article
```
Then you can pass a URL string as argument and the program will retrieve the aforementioned info.
### Standalone
You can use the command-line arguments to pass the URL string to the function as follow:
```
python3 artichoke.py https://domain.com/blog/article/etc
```

## Notes
The scrape_article function's output is a string, you will need to parse it as a JSON to be able to use it elsewhere.

You can use two other function from the program:
- extract_keywords
- summarize_article

They both receive a String as input and output a String as well. Their name is indicative of their function.