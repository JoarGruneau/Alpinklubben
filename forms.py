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
        try:
            password = database.get_user(self.username.data)[0]['hashed_password']
            return check_password_hash(password, self.password.data)
        except:
            return False


class RegisterForm(Form):
    first_name = StringField('first name', [validators.Length(
            min=2, max=25, message='Enter a first name between 2 and 25 characters')],
            render_kw={"placeholder": "First name", "class": "form-control"})

    last_name = StringField('last name', [validators.Length(
            min=2, max=25, message='Enter a last name between 2 and 25 characters')],
            render_kw={"placeholder": "Last name", "class": "form-control"})

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
        database.insert_user(self.first_name.data, self.last_name.data,
                self.username.data, self.email.data, generate_password_hash(self.password.data))


class UpdateForm(Form):
    first_name = StringField('first name', [validators.Length(
            min=2, max=25, message='Enter a first name between 2 and 25 characters')],
            render_kw={"placeholder": "First name", "class": "form-control"})

    last_name = StringField('last name', [validators.Length(
            min=2, max=25, message='Enter a last name between 2 and 25 characters')],
            render_kw={"placeholder": "Last name", "class": "form-control"})

    username = StringField('Username',
                           [validators.Length(
                               min=8, max=25, message='Enter a username between 8 and 25 characters')],
                           render_kw={"placeholder": "username", "class": "form-control"})
    email = EmailField('Email', [validators.DataRequired(), validators.Email()],
                       render_kw={"placeholder": "email", "class": "form-control"})

    def save(self, old_username):
        database.update_user(old_username, self.first_name.data, self.last_name.data, self.username.data, self.email.data)


class PasswordForm(Form):
    password = StringField(
        'Password', [validators.Length(
            min=8, max=25, message='Enter a password between 8 and 25 characters')],
        render_kw={"placeholder": "password", "class": "form-control", "type": "New password", "type": "password"})

    def save(self, username):
        database.update_password(username, generate_password_hash(self.password.data))


class RentForm(Form):
    rent_form = StringField(
        '', default="hours", render_kw={"type": "hidden", "class": "change_form"})
    duration = IntegerField('duration', [validators.DataRequired()], render_kw={"class": "form-control col-md-2"})


class PassForm(Form):
    buyer = StringField(
        '', default="adult", render_kw={"type": "hidden", "class": "change_form"})