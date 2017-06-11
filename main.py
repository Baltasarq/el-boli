# Boli
# GAE application to assist in the process of writing


import webapp2
from webapp2_extras import jinja2


class WelcomePage(webapp2.RequestHandler):
	AnswerPageFile = "answer.html";

	def post(self):
		template_values = {}
		jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **template_values))


app = webapp2.WSGIApplication([
    ('/', WelcomePage),
], debug=True)
