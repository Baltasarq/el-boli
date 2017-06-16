#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import datetime

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import model.section
from model.section import Section


class AddSection(webapp2.RequestHandler):
    def get(self):
        try:
            chapter_id = self.request.GET['chapter_id']
        except:
            self.redirect("/error?msg=missing key for addition")
            return

        user = users.get_current_user()

        if user:
            try:
                chapter = ndb.Key(urlsafe=chapter_id).get()
            except:
                self.redirect("/error?msg=key was not found")
                return

            num_sections = len(Section.query(Section.chapter == chapter.key.id()).fetch(keys_only=True)) + 1
            section = Section()
            section.chapter = chapter.key.id()
            section.num = num_sections
            section.text = "An interesting section."
            key = model.section.update(section)
            self.redirect("/sections/modify?section_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return

app = webapp2.WSGIApplication([
    ("/sections/add", AddSection),
], debug=True)
