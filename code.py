import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
class LoginPage(webapp2.RequestHandler) :
  def get(self) :
    render_template(self, 'index.html', {})
 
class MainPage(webapp2.RequestHandler):
  def post(self) :
    user = users.get_current_user()
    if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, ' + user.nickname())
            #render_template(self, 'infoform.html', {})
    else:
            self.redirect(users.create_login_url(self.request.uri))
            #render_template(self, 'index.html', {})



app = webapp2.WSGIApplication([
  ('/', LoginPage),
  ('/infoform', MainPage),
], debug = True)