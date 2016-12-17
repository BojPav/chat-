#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Chat
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')

            seznam = Chat.query().fetch()
            #params = {"seznam": seznam}

            params = {"seznam": seznam, "logiran": logiran, "logout_url": logout_url, "user": user}
            return self.render_template("hello.html", params=params)
        else:
            logiran = False
            login_url = users.create_login_url('/')

            seznam = Chat.query().fetch()
            #params = {"seznam": seznam}

            params = {"seznam": seznam, "logiran": logiran, "login_url": login_url, "user": user}
            return self.render_template("hello.html", params=params)

        #seznam = Chat.query().fetch()
        #params = {"seznam": seznam}
        #return self.render_template("hello.html", params=params)

    def post(self):
        user = users.get_current_user()
        name = user.nickname()
        message = self.request.get("message")
        #   datum = self.request.get("nastanek")   # datume generira avtomaticno
        new_message = Chat(name=name, message=message)
        new_message.put()
        seznam = Chat.query().fetch()
        #seznam = sorted(seznam)
        params = {"seznam": seznam, "user_nick": name}
        return self.redirect_to("main", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
], debug=True)
