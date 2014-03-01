# Copyright 2014 semnews developers. See the COPYING file at the top-level directory of this
# distribution and at https://www.gnu.org/licenses/gpl.txt.

from urllib.parse import urlparse
from collections import namedtuple
import datetime
import locale
import re

import requests
from bs4 import BeautifulSoup

re_strdate = re.compile(r'\d{1,2} \w{3,10} \d{4}')

Keyword = namedtuple('Keyword', 'slug name')

class Article:
    def __init__(self, url):
        self.url = url
        self.title = ''
        self.text = ''
        self.author = ''
        self.keywords = []
        self.publish_date = None

    def parse(self):
        if 'devoir.com' not in urlparse(self.url).netloc:
            raise ValueError("Invalid URL")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
        self.title = soup('meta', property='og:title')[0].attrs['content'].strip()
        self.text = soup('div', class_='texte')[0].get_text()
        self.keywords = []
        keyword_lis = soup('aside', class_='mots_cles')[0]('li')
        for li in keyword_lis:
            self.keywords.append(Keyword(li.a.attrs['href'].split('/')[-1], li.a.string))
        # Inside the "specs" div, there's 3 splitter-separated fields and the author one is the
        # second. However, the first field is not an "a", so we're in fact looking at the first "a"
        # in the div.
        self.author = soup('div', class_='specs')[0].a.string.strip()
        strdate = soup('div', class_='specs')[0].contents[0].strip()
        # Some date have an hour element, some don't. We use the regexp to simply discard it at all
        # times
        strdate = re_strdate.search(strdate).group()
        try:
            locale.setlocale(locale.LC_ALL, 'fr_CA.UTF-8')
            self.publish_date = datetime.datetime.strptime(strdate, '%d %B %Y').date()
        except (locale.Error, ValueError):
            print("Warning: Could not parse publish time (fr_CA.UTF-8 locale needed)")
