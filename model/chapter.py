#!/usr/bin/env python
# MIT License
# (c) baltasar 2017


from google.appengine.ext import ndb


class Chapter(ndb.Model):
    story = ndb.IntegerProperty(required=True, indexed=True)
    num = ndb.IntegerProperty(required=True, indexed=True)
    added = ndb.DateProperty(auto_now_add=True)
    title = ndb.StringProperty(required=True, indexed=True)
    summary = ndb.TextProperty()


@ndb.transactional
def update(chapter):
    """Updates a chapter.

        :param chapter: The character to chapter.
        :return: The key of the chapter.
    """
    return chapter.put()
