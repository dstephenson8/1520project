import os
import time
import webapp2
import json

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from array import array 
from google.appengine.api import mail
from google.appengine.ext import ndb


###############################################################################
# We'll just use this convenience function to retrieve and render a template.
###############################################################################
def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)


###############################################################################
# This is our user object. It will store the users names, id, phone, email and
# the rides the user has requested or posted
###############################################################################
class UserInfo(ndb.Model):
  # user id of the corresponding instance of User in users api
  uid = ndb.StringProperty(indexed=True)
  # firstname of user
  firstname = ndb.StringProperty(indexed=False)
  # lastname of user
  lastname = ndb.StringProperty(indexed=False)
  # emails is a list because the repeated attribute is equal to True
  phonenumber = ndb.StringProperty(indexed = False)
  email = ndb.StringProperty(indexed=False)



###############################################################################
# This handler redirects the user to login with google, then it sends them to the
# registration page is the user has not registered on this site before, otherwise 
# it sends them to the calendar
###############################################################################
class MainHandler(webapp2.RequestHandler):

  def get(self):
    user = users.get_current_user()
    # checking if user is logged in to google users api
    if user:
      # getting the instance of user info from our own model
      ui = self.getUserInfo(user)
      # checking if exsits or not. If not it means usr is has not done our customize registration
      if ui:
        self.redirect("/calendar")
        # show the usr his/her info since login and registration is done successfully
# >>>>>>>>>>>>THIS IS WHERE IT SHOULD REDIRECT TO THE MAIN PAGE <<<<<<<<<<
        # show user its emails. its a list don't forget (due to reapeted=True)
        # path = os.path.join(os.path.dirname(__file__),"code.py")
      else:
        # user is logged in t google but not registered
        render_template(self, 'register.html', {})
        # render the registration template for user
        # html = template.render(path,{})
        # self.response.write(html)      
    else:
      # user is not logged in to google so redirect him to google's login page
      self.redirect(users.create_login_url("/calendar"))

  # get instance of user info and check if exists
  def getUserInfo(self,user):
    res = UserInfo.query(UserInfo.uid == user.user_id()).fetch()
    if res:
      return res[0]
    else:
      return None


###############################################################################
# This is our register handler which will save the users registration data
###############################################################################
class RegisterHandler(webapp2.RequestHandler):
  #   post function for post method
  def post(self):
    # getting values from request
    firstname = self.request.get("firstname")
    lastname = self.request.get("lastname")
    phonenumber = self.request.get("phonenumber")
    # emails is a list so uses get_all
    email = self.request.get("email")

    # errors is going to contain list of all errors from this form. If is empty it means the form is vbalid
    errors=[]
    # checking if firstanem and lastname exists
    if firstname is None or firstname=="":
      errors+=["First Name missing"]

    if lastname is None or lastname=="":
      errors+=["First Name missing"]

    # checking emails. Note that emails can be empty and in our form its fine,
     # but if not empty they should be in proper format
    

    # if length of errors is zero then form is valid otherwise there are errors
    if len(errors)>0:
      # for error in errors:
      #   self.response.write(error+" <br>")
      self.response.write('<a href="/">Go back</a>')
      
      
    # if no errors in form
    else:
      # save an instance of UserInfo with proper values for its variables
      user = users.get_current_user()
      ui = UserInfo(firstname=firstname,lastname=lastname, phonenumber=phonenumber, email=email,uid=user.user_id())
      # reading all emails form lis
      # finally saving to datastore. If not called nothing will be saved
      ui.put()

      self.redirect("/calendar")



###############################################################################
# This is our meesage post object which stores all the data needed for a ride
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
# This is our save ride handler that handles when a user posts a ride
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
# This handler will be used to set up the post form at postRide.html.
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
# This is our main page handler.  It will show the login screen
###############################################################################
class MainPage(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'MainPage.html',{})



###############################################################################
# displays the calendar
###############################################################################
class calendarHandler(webapp2.RequestHandler):
    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()
        logout = users.create_logout_url('/')


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
              'logout': logout,
            }

            render_template(self, 'calendar.html', template_values)
        else:
            self.redirect(users.create_login_url(self.request.uri))


###############################################################################
# Lists the rides for the date the user has selected
###############################################################################
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
# This is our myRides handler which shows the users the rides they have posts or
# reserved
###############################################################################
class myRidesHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, "myRides.html", {})

###############################################################################
# We have to make sure we map our HTTP request pages to the actual
# RequestHandler objects here.
#
# Note that the first argument to WSGIApplication is an array of tuples; each
# one of these represents one URL-to-RequestHandler pairing.
###############################################################################
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ("/registerpage",MainHandler),
  ("/register",RegisterHandler),
  ('/calendar', calendarHandler),
  ('/list_rides', listRidesHandler),
  ('/postRide', PostRideHandler),
  ('/saveRide', SaveRideHandler),
  ('/myRides', myRidesHandler)
], debug=True)


