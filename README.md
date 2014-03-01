# Semantic annotation of news articles

This program helps you annotate news article with [semantic triples][triples] such as
`(Jean Charest, works_for, McCarthy Tétrault)` from articles like [these][jchired],
`(Pierre Renaud, was_president_of, BAPE)`, `(Pierre Renaud, works_for, McCarthy Tétrault)` and
`(Pierre Renaud, helps, Mining Industry)` from [there][prbape], and so on.

The development of this program is, I hope, one step in the direction of fulfilling the promise of
semantic web, which is the organic emergence of collective intelligence, but since that goal is way
too broad and far away, I have a more immediate goal: Efficiently establish the existence of 
[revolving doors][revolving] in politics.

Of course, I'm not naive enough to think I could develop a program that would find these all by
itself. That would mean deep natural language parsing and understanding, and it would almost need
an artificial intelligence to achieve.

Humans will still drive the revolving door hunting process, but (the way I envision this) as the
human adds annotations that machines can understand better than text, the program knows better and
better where to find data to feed the human detective with, thus making his job much easier.

I'm not sure at all where I'm heading with this, but I'm trying anyway.

## Install & Run

There's no installation process yet. To run the program, you have to download the source and run
it from within the source tree. First, you need to install Python 3.3+, and then, you run:

    $ git clone https://github.com/hsoft/semnews.git
    $ cd semnews
    $ ./bootstrap.sh
    $ . env/bin/activate
    $ python -m semnews

A command prompt will start up, waiting for your commands.

## Usage

For now, the only thing we can do is to fetch and parse articles from [Le Devoir][ledevoir]. You can
do so by typing `analyze <url>`. You'll get a message saying that parsing went ok (or not) and
proving that by printing a bunch of metadata about that article.

Note: We need to parse dates with french month names in them and for now, we use `strptime()` for
this. This means that for date parting to work correctly, you need the `fr_CA.UTF-8` locale
installed on your system.

[triples]: http://en.wikipedia.org/wiki/Triplestore
[jchired]: http://www.ledevoir.com/politique/quebec/368041/jean-charest-se-joint-a-un-cabinet-d-avocats
[prbape]: http://www.ledevoir.com/politique/quebec/378975/l-ancien-president-du-bape-conseille-une-miniere
[revolving]: http://en.wikipedia.org/wiki/Revolving_door_%28politics%29
[ledevoir]: http://www.ledevoir.com/
