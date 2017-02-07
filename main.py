#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form="""
<form method="post">
    <h2>User Signup</h2>
    <table>
        <tr>
        <td>User Name</td>
        <td><input name="user_name" value="%(user_name)s">
        <span style="color:red">%(user_name_error)s</span></td>
        </tr>

        <tr>
        <td>Password</td>
        <!--Value is blank because password is not repeated if they get an error.-->
        <td><input name="password" value="" type="password">
        <span style="color:red">%(password_error)s</span></td>
        </tr>

        <tr>
        <td>Verify Password</td>
        <td><input name="verify_password" value="" type="password">
        <span style="color:red">%(verify_error)s</span></td>
        </tr>

        <tr>
        <td>Email (optional)</td>
        <td><input type="text" name="email" value="%(email)s">
        <span style="color:red">%(email_error)s</span></td>
        </tr>
        <tr>
        <td><input type="submit"></td></tr>
        </tr>
    </table>
</form>
"""

password = re.compile(r"^.{3,20}$")
def valid_password(password):
    return USER_RE.match(password)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return USER_RE.match(user_name)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    #Since email is optional, you use the OR function here to either not return email or return a corrected email -->
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, user_name="", user_name_error="", email="", email_error="", password="", verify_password="", password_error="", verify_error=""):
        self.response.write(form % {"user_name": user_name,
                                        "user_name_error": user_name_error,
                                        "email": email,
                                        "email_error": email_error,
                                        "password": password,
                                        "verify_password": verify_password,
                                        "password_error": password_error,
                                        "verify_error": verify_error
                                        })

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        user_name = self.request.get('user_name')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email = self.request.get('email')

        params = dict(user_name = user_name, email = email)

        if not valid_username(user_name):
            params['user_name_error'] = "That is not a valid username."
            have_error = True

        if not valid_password(password):
            params['password_error'] = "That is not a valid password."
            have_error = True
        elif password != verify_password:
            have_error = True
            params['verify_error'] = "Your passwords do not match."

        if not valid_email(email):
            params['email_error'] = "That's not a valid email."
            have_error = True

        if have_error == True:
            self.write_form(**params)
        else:
            self.redirect('/welcome?user_name=' + user_name)

class Welcome(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('user_name')
        if valid_username(user_name):
            self.response.write('<h1>Welcome, %s!' % user_name)


app = webapp2.WSGIApplication([('/', MainHandler),
('/welcome', Welcome)],
 debug=True)
