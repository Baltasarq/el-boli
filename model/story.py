#!/usr/bin/env python
# MIT License
# (c) baltasar 2017


from google.appengine.ext import ndb


class Story(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True)
    user = ndb.StringProperty(required=True, indexed=True)
    title = ndb.StringProperty(required=True, indexed=True)
    subtitle  = ndb.StringProperty(required=True, indexed=True)
    summary = ndb.TextProperty()


@ndb.transactional
def update(story):
    """Updates a story.
    
        :param story: The story to update.
        :return: The key of the story.
    """
    return story.put()
