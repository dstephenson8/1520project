import os
import time
import webapp2
import json

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from array import array #allow us to use arrays

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
  day = db.StringProperty()
  month = db.StringProperty()
  year = db.StringProperty()
  
  # we will use this method to automatically output a formatted time string.
  def formatted_time(self):
    return time.ctime(self.time)
  

###############################################################################
# This handler will be used to set up the post form at post.html.
###############################################################################
class PostRideHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/')
    logout = users.create_logout_url('/')
    day = self.request.get('day')
    month = self.request.get('month')
    year = self.request.get('year')

    template_values = {
      'login': login,
      'logout': logout,
      'user': user,
      'day': day,
      'month': month,
      'year': year,
    }
    render_template(self, 'postRide.html', template_values)
    

###############################################################################
# This is our main page handler.  It will show the MessagePost objects in 
# the index.html page.
###############################################################################


class MainPage(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'MainPage.html',{})

class calendarHandler(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        if user:
            query = MessagePost.all()
            posts = list()

            #Create all of the data that needs to be passed
            day_num = []
            month_str = ["Janurary", "February", "March", "April", "May", "June", "July", "August", "September", "October" "November", "December"]
            month_num = []
            year_num = []
            depart_city = []
            arrive_city = []
            depart_time = []

            for post in query.run():
                day_num.append(int(post.day))
                
                month = post.month;
                j = 0
                while month != month_str[j]:
                  j+=1

                month_num.append(j)
                year_num.append(int(post.year))
                depart_city.append(post.depart)
                depart_time.append(post.time)
                arrive_city.append(post.arrive)

            template_values = {
              'day_num': day_num,
              'month_num': month_num,
              'year_num': year_num,
              'depart_city': json.dumps(depart_city),
              'depart_time': json.dumps(depart_time),
              'arrive_city': json.dumps(arrive_city),
            }

            render_template(self, 'calendar.html', template_values)
        else:
            self.redirect(users.create_login_url(self.request.uri))


class listRidesHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/')
    logout = users.create_logout_url('/')
    posts = list()
    query = MessagePost.all()
    query.order('-time')
    day = self.request.get('day')
    month = self.request.get('month')
    year = self.request.get('year')

    for post in query.run():
      if post.day == day and post.month == month and post.year == year:
        posts.append(post)
    
    template_values = {
      'login': login,
      'logout': logout,
      'user': user,
      'posts': posts,
      'day': day,
      'month': month,
      'year': year,
    }
    render_template(self, 'listing_Of_Rides.html', template_values)

    
###############################################################################
# This will handle the form submission, then redirect the user to the list rides page
###############################################################################
class SaveRideHandler(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      post = MessagePost()
      post.depart = self.request.get('depart')
      post.arrive = self.request.get('arrive')
      post.timeofdepart = self.request.get('timeofdepart')
      post.seats = self.request.get('seats')
      post.day = self.request.get('day')
      post.month = self.request.get('month')
      post.year = self.request.get('year')
      post.message_text = self.request.get('text')
      post.user = user.email()
      post.time = int(time.time())
      post.put()

      day = self.request.get('day')
      month = self.request.get('month')
      year = self.request.get('year')

    self.redirect('/list_rides?day='+day+'&month='+month+'&year='+year)
    
###############################################################################
# We have to make sure we map our HTTP request pages to the actual
# RequestHandler objects here.
#
# Note that the first argument to WSGIApplication is an array of tuples; each
# one of these represents one URL-to-RequestHandler pairing.
###############################################################################
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/calendar', calendarHandler),
  ('/list_rides', listRidesHandler),
  ('/postRide', PostRideHandler),
  ('/saveRide', SaveRideHandler)
], debug=True)

