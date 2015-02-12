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

class ProcessForm(webapp2.RequestHandler):
  def post(self):
    render_template(self, 'infoform.html', {})


class ProcessForm2(webapp2.RequestHandler):
  def post(self):
    fname = self.request.get('fname')
    lname = self.request.get('lname')
    phonenumber = self.request.get('phonenumber')
    email = self.request.get('email')
    prefer_contact = self.request.get('prefer_contact')
    fname = self.request.get('fname')
    year = self.request.get('year')
    availseats = self.request.get('availseats')
    departcity = self.request.get('departcity')
    arrivecity = self.request.get('arrivecity')
    time = self.request.get('time')

   
    render_template(self, 'day.html',{
     "fname": fname,
     "lname": lname
    # "mynumber2": number2,
    #"number3": number3
  })
  
  def get(self):
	render_template(self, 'day.html', {})



app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/processform', ProcessForm),
  ('/processform2', ProcessForm2),
  ('/list_rides', ProcessForm2),
], debug = True)

