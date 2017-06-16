#!/usr/bin/env python
# MIT License
# (c) baltasar 2017


from google.appengine.ext import ndb


class Section(ndb.Model):
    chapter = ndb.IntegerProperty(required=True, indexed=True)
    added = ndb.DateProperty(auto_now_add=True)
    num = ndb.IntegerProperty(required=True, indexed=True)
    text = ndb.TextProperty()


@ndb.transactional
def update(section):
    """Updates a section.

        :param par: The section to update.
        :return: The key of the section.
    """
    return section.put()
