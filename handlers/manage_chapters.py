# Boli
# GAE application to assist in the process of writing
# Manage chapters inside a story


import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from model.appinfo import AppInfo
from model.story import Story
from model.chapter import Chapter

from stories.stats import count


class ChaptersManager(webapp2.RequestHandler):
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
            chapters = Chapter.query(
                    Chapter.story == story.key.id()).order(Chapter.num)
            access_link = users.create_logout_url("/")
            total_stats = count(story.key.id())

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "chapters": chapters,
                "total_crs": total_stats["crs"],
                "total_ws": total_stats["ws"],
                "total_pgs": total_stats["pgs"]
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("chapters.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_chapters', ChaptersManager),
], debug=True)
