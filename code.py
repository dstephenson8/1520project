import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
class MainPage(webapp2.RequestHandler) :
  def get(self) :
    render_template(self, 'index.html', {})
  #   user = users.get_current_user()
  #   logout_url = ''
  #   login_url = ''

  #   if user:
  #     logout_url = users.get_logout_url('/')
  #     response.out.write('To log out go to' + logout_url)
	 # else:
	 #   login_url = users.get_login_url('/')
	 #   response.out.write('to login goto' + login_url)
    

app = webapp2.WSGIApplication([
  ('/', MainPage)
])