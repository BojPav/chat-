from google.appengine.ext import ndb


class Chat(ndb.Model):
    name = ndb.StringProperty()
    message = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)