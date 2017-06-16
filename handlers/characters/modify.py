#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.story import Story
from model.character import Character
from model.appinfo import AppInfo


class ModifyCharacter(webapp2.RequestHandler):
    def get(self):
        try:
            character_id = self.request.GET['character_id']
        except:
            self.redirect("/error?msg=key was not found")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                character = ndb.Key(urlsafe=character_id).get()
                story = Story.get_by_id(character.story)
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "character": character
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modify_character.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            character_id = self.request.GET['character_id']
        except:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()

        if user:
            # Get story by key
            try:
                character = ndb.Key(urlsafe=character_id).get()
                story = Story.get_by_id(character.story)
            except:
                self.redirect("/error?msg=key does not exist")
                return

            character.name = self.request.get("name", "").strip()
            character.summary = self.request.get("summary", "").strip()

            # Chk
            if len(character.name) < 1:
                self.redirect("/error?msg=Aborted modification: missing name")
                return

            # Chk title
            existing_characters = Character.query(Character.name == character.name)
            if  (existing_characters
             and existing_characters.count() > 0
             and existing_characters.get() != character):
                self.redirect("/error?msg=Character with name \""
                            + character.title.encode("ascii", "replace")
                            + "\" already exists.")
                return

            # Save
            character.put()
            self.redirect("/info?msg=Character modified: \""
                + character.name.encode("ascii", "replace")
                + "@" + story.title.encode("ascii", "replace")
                + "\"&url=/manage_characters?story_id=" + story.key.urlsafe())
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/characters/modify", ModifyCharacter),
], debug=True)
