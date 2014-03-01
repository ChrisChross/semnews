# Copyright 2014 semnews developers. See the COPYING file at the top-level directory of this
# distribution and at https://www.gnu.org/licenses/gpl.txt.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    url = Column(String, unique=True)
    title = Column(String)
    author = Column(String)
    publish_date = Column(Date)
    text = Column(Text)

    source = relationship('Source', backref='articles')

class ArticleKeyword(Base):
    __tablename__ = 'article_keywords'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    slug = Column(String)
    name = Column(String)

    article = relationship('Article', backref='keywords')

    def __repr__(self):
        return "%s / %s" % (self.slug, self.name)

engine = None
session = None
ledevoir = None

def opendb():
    global engine, session, ledevoir
    engine = create_engine('sqlite:///semnews.db')
    session = sessionmaker(bind=engine)()
    try:
        session.query(Source).all()
    except OperationalError:
        print("DB not created yet. Creating...")
        Base.metadata.create_all(engine)
    try:
        ledevoir = session.query(Source).filter_by(name='ledevoir').one()
    except NoResultFound:
        print("Source \"ledevoir\" not there. Creating...")
        ledevoir = Source(name='ledevoir')
        session.add(ledevoir)
        session.commit()
