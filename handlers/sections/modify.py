#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import datetime
import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.section
from model.story import Story
from model.chapter import Chapter
from model.character import Character
from model.appinfo import AppInfo


class ModifySection(webapp2.RequestHandler):
    def get(self):
        try:
            section_id = self.request.GET['section_id']
        except:
            self.redirect("/error?msg=missing key for modification")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                section = ndb.Key(urlsafe=section_id).get()
                chapter = Chapter.get_by_id(section.chapter)
                story = Story.get_by_id(chapter.story)
                characters = Character.query(Character.story == story.key.id())
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "characters": characters,
                "chapter": chapter,
                "section": section
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modify_section.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            section_id = self.request.GET['section_id']
        except:
            self.redirect("/error?msg=missing key for modification")
            return

        user = users.get_current_user()

        if user:
            try:
                section = ndb.Key(urlsafe=section_id).get()
                chapter = Chapter.get_by_id(section.chapter)
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=key does not exist")
                return

            section.text = self.request.get("text", "").strip()

            # Chk
            if len(section.text) < 1:
                self.redirect("/error?msg=Aborted modification: missing section's text")
                return

            if section.num < 1:
                self.redirect("/error?msg=Aborted modification: missing section's number")
                return

            # Save
            model.section.update(section)
            self.redirect("/info?msg=Section modified: \""
                + (story.title + ": " + chapter.title).encode("ascii", "replace") + ": " + str(section.num)
                + "\"&url=/manage_sections?chapter_id=" + chapter.key.urlsafe())
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/sections/modify", ModifySection),
], debug=True)
