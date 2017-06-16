# Boli
# GAE application to assist in the process of writing
# Manage characters inside a story


import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb


from model.appinfo import AppInfo
from model.story import Story
from model.character import Character


class CharactersManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            user_name = user.nickname()

            try:
                id = self.request.GET['story_id']
            except:
                id = None

            if not id:
                self.redirect("/error?msg=Key missing for management.")
                return

            story = ndb.Key(urlsafe=id).get()
            characters = Character.query(Character.story == story.key.id()).order(Character.name)
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "characters": characters
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("characters.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_characters', CharactersManager),
], debug=True)
