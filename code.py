import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
class MainPage(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            render_template(self, 'calendar.html', {})
        else:
            self.redirect(users.create_login_url(self.request.uri))



app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug = True)

