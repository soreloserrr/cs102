import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    news_body = parser.body.center.table.findAll("tr")[3]
    news_body = news_body.findAll("tr")

    for i in range(0, len(news_body) - 2, 3):
        item = news_body[i]

        item = item.findAll("td")[2]
        details = news_body[i + 1]

        url = "/".join(item.a["href"].split("/")[:3])
        title = item.a.text
        points = int(details.span.text.split()[0])
        author = details.a.text

        comments = details.findAll("a")[-1].text
        if comments == "discuss":
            comments = 0
        else:
            comments = int(comments.split()[0])
        news_list.append({"author": author, "comments": comments, "points": points, "title": title, "url": url})

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    body = parser.body.center.table.findAll("tr")[-3]
    return body.a["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "main":
    news = get_news("https://news.ycombinator.com/newest", 2)
    print(len(news))
    print(news[:3])
