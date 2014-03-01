#!/usr/bin/env python
# Copyright 2014 semnews developers. See the COPYING file at the top-level directory of this
# distribution and at https://www.gnu.org/licenses/gpl.txt.

import cmd

from .article import get_article
from . import db

class SemnewsCmd(cmd.Cmd):
    intro = "Welcome to Semnews. Type help or ? to list commands.\n"
    prompt = "semnews> "

    def preloop(self):
        db.opendb()
        self.article = None

    def do_analyze(self, arg):
        """analyze <url>:
        Fetches and parses article at <url> and prints out a bunch of metadata extracted from it.
        """
        try:
            a = get_article(arg)
        except ValueError:
            print("Invalid URL (Only Le Devoir articles supported for now).")
        print("Now working on \"%s\"" % a.title)
        print("Author: %s" % a.author)
        print("Published at: %s" % a.publish_date)
        print("Keywords: %s" % a.keywords)
        print("%d statements made about this article" % len(a.statements))
        self.article = a

    def do_state(self, arg):
        """state:
        Make a statement. You'll be prompted for an subject, a predicate, and an object.
        """
        if self.article is None:
            print("No active article. Aborting.")
            return
        subject = input("Subject: ")
        subject = db.Entity.get_or_create(subject, db.session)
        predicate = input("Predicate: ")
        object = input("Object: ")
        object = db.Entity.get_or_create(object, db.session)
        statement = db.Statement(
            article=self.article, subject=subject, predicate=predicate, object=object
        )
        db.session.add(statement)
        db.session.commit()

    def do_EOF(self, arg):
        print("Goodbye!")
        return True

if __name__ == '__main__':
    SemnewsCmd().cmdloop()
