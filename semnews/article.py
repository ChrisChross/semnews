# Copyright 2014 semnews developers. See the COPYING file at the top-level directory of this
# distribution and at https://www.gnu.org/licenses/gpl.txt.

from urllib.parse import urlparse
import datetime
import locale
import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound

from . import db

re_strdate = re.compile(r'\d{1,2} \w{3,10} \d{4}')

def get_article(url):
    try:
        article = db.session.query(db.Article).filter_by(url=url).one()
        print("Already in cache, no need to fetch")
        return article
    except db.NoResultFound:
        print("Fetching article...")
    if 'devoir.com' not in urlparse(url).netloc:
        raise ValueError("Invalid URL")
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = soup('meta', property='og:title')[0].attrs['content'].strip()
    text = soup('div', class_='texte')[0].get_text()
    keywords = []
    keyword_lis = soup('aside', class_='mots_cles')[0]('li')
    for li in keyword_lis:
        k = db.ArticleKeyword(slug=li.a.attrs['href'].split('/')[-1], name=li.a.string)
        keywords.append(k)
    # Inside the "specs" div, there's 3 splitter-separated fields and the author one is the
    # second. However, the first field is not an "a", so we're in fact looking at the first "a"
    # in the div.
    author = soup('div', class_='specs')[0].a.string.strip()
    strdate = soup('div', class_='specs')[0].contents[0].strip()
    # Some date have an hour element, some don't. We use the regexp to simply discard it at all
    # times
    strdate = re_strdate.search(strdate).group()
    try:
        locale.setlocale(locale.LC_ALL, 'fr_CA.UTF-8')
        publish_date = datetime.datetime.strptime(strdate, '%d %B %Y').date()
    except (locale.Error, ValueError):
        print("Warning: Could not parse publish time (fr_CA.UTF-8 locale needed)")
    article = db.Article(
        source=db.ledevoir, url=url, title=title, author=author, publish_date=publish_date,
        text=text, keywords=keywords
    )
    db.session.add(article)
    db.session.commit()
    return article
