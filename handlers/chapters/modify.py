#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import datetime
import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.chapter
from model.story import Story
from model.chapter import Chapter
from model.appinfo import AppInfo


class ModifyChapter(webapp2.RequestHandler):
    def get(self):
        try:
            chapter_id = self.request.GET['chapter_id']
        except:
            self.redirect("/error?msg=missing key for modifying")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                chapter = ndb.Key(urlsafe=chapter_id).get()
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "chapter": chapter,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modify_chapter.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            chapter_id = self.request.GET['chapter_id']
        except:
            self.redirect("/error?msg=missing key for modifying")
            return

        user = users.get_current_user()

        if user:
            # Get story and chapter by key
            try:
                chapter = ndb.Key(urlsafe=chapter_id).get()
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=key does not exist")
                return

            chapter.title = self.request.get("title", "").strip()
            chapter.summary = self.request.get("summary", "").strip()

            # Chk
            if len(chapter.title) < 1:
                self.redirect("/error?msg=Aborted modification: missing title")
                return

            # Chk title
            existing_chapters = Chapter.query(Chapter.title == chapter.title)
            if  (existing_chapters
             and existing_chapters.count() > 0
             and existing_chapters.get() != chapter):
                self.redirect("/error?msg=Chapter with title \""
                            + chapter.title.encode("ascii", "replace")
                            + "\" already exists.")
                return

            # Save
            model.chapter.update(chapter)
            self.redirect("/info?msg=Chapter modified: \""
                + (story.title + ": " + chapter.title).encode("ascii", "replace")
                + "\"&url=/manage_chapters?story_id=" + story.key.urlsafe())
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/chapters/modify", ModifyChapter),
], debug=True)
