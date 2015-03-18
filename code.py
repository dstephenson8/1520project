import os
import time
import webapp2
import json

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from array import array #allow us to use arrays
from google.appengine.api import mail

###############################################################################
# We'll just use this convenience function to retrieve and render a template.
def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)


###############################################################################
class MessagePost(db.Model):

  depart_address = db.StringProperty()
  depart_city = db.StringProperty()
  depart_state = db.StringProperty()
  depart_zip = db.StringProperty()
  depart_time = db.StringProperty()
  arrive_address = db.StringProperty()
  arrive_city = db.StringProperty()
  arrive_state = db.StringProperty()
  arrive_zip = db.StringProperty()
  car_model = db.StringProperty()
  car_year = db.StringProperty()
  numSeats = db.IntegerProperty()
  message = db.StringProperty(multiline=True)
  time = db.IntegerProperty()
  user = db.StringProperty()
  day = db.StringProperty()
  month = db.StringProperty()
  year = db.StringProperty()
  nickname = db.StringProperty()
  
  # we will use this method to automatically output a formatted time string.
  def formatted_time(self):
    return time.ctime(self.time)


###############################################################################
# This will handle the form submission, then redirect the user to the list rides page
###############################################################################
class SaveRideHandler(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      post = MessagePost()
      post.depart_address = self.request.get('depart_address')
      post.depart_city = self.request.get('depart_city')
      post.depart_state = self.request.get('depart_state')
      post.depart_zip = self.request.get('depart_zip')
      post.depart_time = self.request.get('depart_time')
      post.arrive_address = self.request.get('arrive_address')
      post.arrive_city = self.request.get('arrive_city')
      post.arrive_state = self.request.get('arrive_state')
      post.arrive_zip = self.request.get('arrive_zip')
      post.day = self.request.get('day')
      post.month = self.request.get('month')
      post.year = self.request.get('year')
      post.car_model = self.request.get('car_model')
      post.car_year = self.request.get('car_year')
      post.numSeats = int(self.request.get('numSeats'))
      post.message = self.request.get('message')
      post.user = user.email()
      post.time = int(time.time())
      post.nickname = user.nickname()
      post.put()

      day = self.request.get('day')
      month = self.request.get('month')
      year = self.request.get('year')

    message = mail.EmailMessage(sender="<1520GroupL@gmail.com>", subject="Your posted ride")
    message.to = user.email()
    message.body = """
    Dear Sharer,

      Your ride has been successfully posted! Thank you for using Ride Sharer.

    The Ride Sharer Team
    """
    message.send()

    self.redirect('/list_rides?day='+day+'&month='+month+'&year='+year)



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
                while month != month_str[j] and j <= 11:
                  j+=1

                month_num.append(j)
                year_num.append(int(post.year))
                depart_city.append(post.depart_city)
                depart_time.append(post.time)
                arrive_city.append(post.arrive_city)

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
    
    if(len(posts) == 0):
      noRides = True;
    else:
      noRides = False;

    template_values = {
      'login': login,
      'logout': logout,
      'user': user,
      'posts': posts,
      'day': day,
      'month': month,
      'year': year,
      'noRides': noRides,
    }
    render_template(self, 'listing_Of_Rides.html', template_values)

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
  ('/saveRide', SaveRideHandler),
], debug=True)


