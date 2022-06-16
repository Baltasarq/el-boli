#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import webapp2
from google.appengine.ext import ndb
from webapp2_extras import jinja2
from google.appengine.api import users

from model.appinfo import AppInfo
from model.chapter import Chapter
from model.story import Story
from model.section import Section


class ExportStory(webapp2.RequestHandler):
    def get(self):
        id = self.request.GET.get('story_id')

        if not id:
            self.redirect("/error?msg=Key missing for exporting.")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                story = ndb.Key(urlsafe=id).get()

                # Collect all chapters
                chapters = Chapter.query(
                    Chapter.story == story.key.id()).order(Chapter.num)

                # Collect all sections
                all_sections = {}
                for chapter in chapters:
                    # Retrieve all sections
                    sections = Section.query(
                        Section.chapter == chapter.key.id()).order(Section.num).fetch()

                    all_sections[chapter.num] = sections
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "chapters": chapters,
                "all_sections": all_sections
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.headers["target"] = "_blank"
            self.response.write(jinja.render_template("export_story.html", **template_values));
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/stories/export", ExportStory),
], debug=True)
