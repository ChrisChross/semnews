#!/usr/bin/env python
# Copyright 2014 semnews developers. See the COPYING file at the top-level directory of this
# distribution and at https://www.gnu.org/licenses/gpl.txt.

import cmd

from .article import Article

class SemnewsCmd(cmd.Cmd):
    intro = "Welcome to Semnews. Type help or ? to list commands.\n"
    prompt = "semnews> "

    def do_analyze(self, arg):
        """analyze <url>:
        Fetches and parses article at <url> and prints out a bunch of metadata extracted from it.
        """
        a = Article(arg)
        try:
            a.parse()
        except ValueError:
            print("Invalid URL (Only Le Devoir articles supported for now).")
        print("Parsing of \"%s\" successful" % a.title)
        print("Author: %s" % a.author)
        print("Published at: %s" % a.publish_date)
        print("Keywords: %s" % a.keywords)

    def do_EOF(self, arg):
        print("Goodbye!")
        return True

if __name__ == '__main__':
    SemnewsCmd().cmdloop()
