#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.remove_data
from model.appinfo import AppInfo
from model.story import Story
from model.chapter import Chapter
from model.section import Section


class DeleteSection(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['section_id']
        except:
            self.redirect("/error?msg=Key missing for deletion.")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                section = ndb.Key(urlsafe=id).get()
                chapter = Chapter.get_by_id(section.chapter)
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
                "section": section
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("delete_section.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            section_id = self.request.GET['section_id']
        except:
            self.redirect("/error?msg=Key missing for deletion.")
            return

        user = users.get_current_user()

        if user:
            try:
                section = ndb.Key(urlsafe=section_id).get()
                chapter = Chapter.get_by_id(section.chapter)
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            self.redirect("/info?msg=Section deleted: "
                + story.title.encode("ascii", "replace")
                    + ": " + chapter.title.encode("ascii", "replace")
                    + " - " + str(section.num)
                + "&url=/manage_sections?chapter_id=" + chapter.key.urlsafe())

            # Remove story
            model.remove_data.remove_section(section.key)
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/sections/delete", DeleteSection),
], debug=True)
