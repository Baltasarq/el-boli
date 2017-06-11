#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import datetime

import webapp2
from google.appengine.api import users

from model.story import Story


class AddStory(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        num_stories = Story.query().count()

        if user:
            story = Story()
            story.user = user.user_id()
            story.title = "Untitled " + str(num_stories)
            story.subtitle = "A new story."
            story.summary = "An awesome story."
            key = story.put()
            self.redirect("/stories/modify?story_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return

app = webapp2.WSGIApplication([
    ("/stories/add", AddStory),
], debug=True)
