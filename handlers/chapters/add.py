#!/usr/bin/env python
# MIT License
# (c) baltasar 2016


import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import model.chapter
from model.chapter import Chapter


class AddChapter(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['story_id']
        except:
            self.redirect("/error?msg=story was not found")
            return

        user = users.get_current_user()

        if user:
            try:
                story = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            num_chapters = len(Chapter.query(Chapter.story == story.key.id()).fetch(keys_only=True)) + 1

            chapter = Chapter()
            chapter.story = story.key.id()
            chapter.num = num_chapters
            chapter.title = "Untitled " + str(num_chapters)
            chapter.summary = "An awesome chapter."
            key = model.chapter.update(chapter)
            self.redirect("/chapters/modify?story_id=" + story.key.urlsafe()
                            + "&chapter_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return

app = webapp2.WSGIApplication([
    ("/chapters/add", AddChapter),
], debug=True)
