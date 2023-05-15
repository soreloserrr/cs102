from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news

bayes = NaiveBayesClassifier(alpha=0.05)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label.is_(None)).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.params.get("label", "")
    news_id = request.params.get("id")
    s.query(News).filter(News.id == news_id).update({News.label: label})
    s.commit()
    if __name__ == "__main__":
        redirect("/news")


@route("/update")
def update_news():
    s = session()
    try:
        news = get_news("https://news.ycombinator.com/newest", 1)
        for i in news:
            entry = s.query(News).filter(News.title == i["title"]).first()
            if not entry:
                entry = News(
                    title=i["title"],
                    author=i["author"],
                    url=i["url"],
                    comments=i["comments"],
                    points=i["points"],
                )
                s.merge(entry)
    except Exception as e:
        print(f"Error updating news: {str(e)}")
        s.rollback()
    else:
        s.commit()
    finally:
        s.close()

    if __name__ == "__main__":
        redirect("/news")



@route("/classify")
def classify_news():
    s = session()
    labled_news = s.query(News).filter(News.label.isnot(None)).all()
    x = [i.title for i in labled_news]
    y = [i.label for i in labled_news]
    bayes.fit(x, y)
    unlabled_news = s.query(News).filter(News.label.is_(None)).all()
    X = [i.title for i in unlabled_news]
    y = bayes.predict(X)
    for item, label in zip(unlabled_news, y):
        item.label = label
    s.commit()
    sorted_news = sorted(unlabled_news, key=lambda x: x.label)
    return sorted_news


@route("/recommendations")
def recommendations():
    s = session()
    news = s.query(News).filter(News.label.is_(None)).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for item, label in zip(news, y):
        item.label = label
    s.commit()
    sorted_news = sorted(news, key=lambda x: x.label)
    return template("news_template", rows=sorted_news)



if __name__ == "__main__":
    run(host="localhost", port=8080, debug=False)
