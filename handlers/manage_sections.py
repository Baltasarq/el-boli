# Boli
# GAE application to assist in the process of writing
# Manage sections inside a story


import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb


from model.appinfo import AppInfo
from model.story import Story
from model.chapter import Chapter
from model.section import Section

from stories.stats import count_chapter


class SectionsManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            user_name = user.nickname()

            try:
                chapter_id = self.request.GET['chapter_id']
            except:
                self.redirect("/error?msg=Key missing for management.")
                return

            try:
                chapter = ndb.Key(urlsafe=chapter_id).get()
                story = Story.get_by_id(chapter.story)
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            sections = Section.query(
                Section.chapter == chapter.key.id()).order(Section.num)
            total_stats = count_chapter(chapter.key.id())
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
                "chapter": chapter,
                "sections": sections,
                "total_crs": total_stats["crs"],
                "total_ws": total_stats["ws"],
                "total_pgs": total_stats["pgs"]
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("sections.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_sections', SectionsManager),
], debug=True)
