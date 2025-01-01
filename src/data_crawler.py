
from bs4 import BeautifulSoup
import httpx

def data_crawling_fn(url: str) -> str:
    """
        Following function send request to given url and extract 2 useful info
        Article title and Article text

        str, eg. title$text

        resultant string will be seperated by delimeter '$'
    """

    print("=======" * 12)
    print("Data Crawling Started...")
    print("=======" * 12)

    html = httpx.get(url)
    soup = BeautifulSoup(html, "html.parser")

    # Article title
    title = soup.find('h1', class_="entry-title").text

    # Article text
    article_text = soup.find('div', class_="td-post-content").text

    article_data = title.strip() + "$" + article_text.strip()

    # print(article_data)

    return article_data