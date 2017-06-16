#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import model.character
from model.character import Character


class AddCharacter(webapp2.RequestHandler):
    def get(self):
        try:
            story_id = self.request.GET['story_id']
        except:
            self.redirect("/error?msg=missing key")
            return

        user = users.get_current_user()

        if user:
            try:
                story = ndb.Key(urlsafe=story_id).get()
            except:
                self.redirect("/error?msg=key was not found")
                return

            num_characters = len(Character.query().fetch(keys_only=True)) + 1
            character = Character()
            character.story = story.key.id()
            character.name = "John Doe " + str(num_characters)
            character.summary = "An awesome character."
            key = model.character.update(character)
            self.redirect("/characters/modify?character_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return

app = webapp2.WSGIApplication([
    ("/characters/add", AddCharacter),
], debug=True)
