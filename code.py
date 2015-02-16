import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

###############################################################################
# We'll just use this convenience function to retrieve and render a template.
def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)


###############################################################################
class MessagePost(db.Model):
  depart = db.StringProperty()
  arrive = db.StringProperty()
  timeofdepart = db.StringProperty()
  seats = db.StringProperty()
  message_text = db.StringProperty(multiline=True)
  time = db.IntegerProperty()
  user = db.StringProperty()
  
  # we will use this method to automatically output a formatted time string.
  def formatted_time(self):
    return time.ctime(self.time)
  

###############################################################################
# This handler will be used to set up the post form at post.html.
###############################################################################
class PostPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/')
    logout = users.create_logout_url('/')
    template_values = {
      'login': login,
      'logout': logout,
      'user': user
    }
    render_template(self, 'post.html', template_values)
    

###############################################################################
# This is our main page handler.  It will show the MessagePost objects in 
# the index.html page.
###############################################################################


class MainPage(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            render_template(self, 'calendar.html', {})
        else:
            self.redirect(users.create_login_url(self.request.uri))





class MainPage2(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/')
    logout = users.create_logout_url('/')
    posts = list()
    query = MessagePost.all()
    query.order('-time')
    for post in query.run():
      posts.append(post)
    
    template_values = {
      'login': login,
      'logout': logout,
      'user': user,
      'posts': posts
    }
    render_template(self, 'day2.html', template_values)

    
###############################################################################
# This will handle the form submission, then redirect the user to the main 
# page.
###############################################################################
class SavePostPage(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      post = MessagePost()
      post.depart = self.request.get('depart')
      post.arrive = self.request.get('arrive')
      post.timeofdepart = self.request.get('timeofdepart')
      post.seats = self.request.get('seats')


      post.message_text = self.request.get('text')
      post.user = user.email()
      post.time = int(time.time())
      post.put()
    self.redirect('/')
    
###############################################################################
# We have to make sure we map our HTTP request pages to the actual
# RequestHandler objects here.
#
# Note that the first argument to WSGIApplication is an array of tuples; each
# one of these represents one URL-to-RequestHandler pairing.
###############################################################################
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/list_rides', MainPage2),
  ('/savepost', SavePostPage),
  ('/post', PostPage)
], debug=True)

