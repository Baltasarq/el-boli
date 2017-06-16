#!/usr/bin/env python
# MIT License
# (c) baltasar 2017


from google.appengine.ext import ndb


class Character(ndb.Model):
    story = ndb.IntegerProperty(required=True, indexed=True)
    added = ndb.DateProperty(auto_now_add=True)
    name = ndb.StringProperty(required=True, indexed=True)
    summary = ndb.TextProperty()


@ndb.transactional
def update(character):
    """Updates a character.

        :param character: The character to update.
        :return: The key of the character.
    """
    return character.put()
