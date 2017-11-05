from wtforms import Form, StringField, SelectField, IntegerField, validators
from wtforms.fields.html5 import EmailField
from werkzeug.security import generate_password_hash, \
     check_password_hash

import database


class LoginForm(Form):
    username = StringField('username',
                           [validators.Length(min=8, max=25, message='Enter a username between 8 and 25 characters')],
                           render_kw={"placeholder": "username", "class": "form-control"})
    password = StringField(
        'Password', [validators.Length(
            min=8, max=25, message='Enter a password between 8 and 25 characters')],
        render_kw={"placeholder": "password", "class": "form-control", "type": "password"})

    def authenticate(self):
        password = database.get_user(self.username.data)
        if len(password) > 0:
            return check_password_hash(
                database.get_user(self.username.data)[0], self.password.data)
        else:
            return False


class RegisterForm(Form):
    username = StringField('Username',
                           [validators.Length(
                               min=8, max=25, message='Enter a username between 8 and 25 characters')],
                           render_kw={"placeholder": "username", "class": "form-control"})
    email = EmailField('Email', [validators.DataRequired(), validators.Email()],
                       render_kw={"placeholder": "email", "class": "form-control"})
    password = StringField(
        'Password', [validators.Length(
            min=8, max=25, message='Enter a password between 8 and 25 characters')],
        render_kw={"placeholder": "password", "class": "form-control", "type": "password"})

    def save(self):
        print ("medadadsa")
        database.insert_user(
                self.username.data, self.email.data, generate_password_hash(self.password.data))
        print("done")


class RentForm(Form):
    rent_form = StringField(
        '', default="hours", render_kw={"type": "hidden", "class": "change_form"})
    duration = IntegerField('duration', [validators.DataRequired()], render_kw={"class": "form-control col-md-2"})

class PassForm(Form):
    buyer = StringField(
        '', default="adult", render_kw={"type": "hidden", "class": "change_form"})