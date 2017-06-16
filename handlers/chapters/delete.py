#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.remove_data
from model.appinfo import AppInfo
from model.story import Story


class DeleteChapter(webapp2.RequestHandler):
    def get(self):
        try:
            chapter_id = self.request.GET['chapter_id']
        except:
            self.redirect("/error?msg=Key missing for deletion (get).")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                chapter = ndb.Key(urlsafe=chapter_id).get()
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "chapter": chapter,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("delete_chapter.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['chapter_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=Key missing for deletion (post).")
            return

        user = users.get_current_user()

        if user:
            try:
                chapter = ndb.Key(urlsafe=id).get()
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=Key was not found for deletion.")
                return

            self.redirect("/info?msg=Chapter deleted: "
                + (story.title + ": " + chapter.title).encode("ascii", "replace")
                + "&url=/manage_chapters?story_id=" + story.key.urlsafe())

            # Remove chapter
            model.remove_data.remove_chapter(chapter.key)
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/chapters/delete", DeleteChapter),
], debug=True)
