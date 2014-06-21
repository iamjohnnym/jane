from flask.ext.wtf import Form
from wtforms import SelectField, TextAreaField, TextField, PasswordField, BooleanField, validators, ValidationError
from wtforms.validators import Required
from app.modules.domain.main import Domain


class UserForm(Form):
    first_name = TextField('First name')
    last_name = TextField('Last name')
    email = TextField('Email', [validators.Email(message="Please provide a valid email address")])
    shell = SelectField('Shell',
                        choices=[('/bin/false','/bin/false'),
                                 ('/bin/bash', '/bin/bash')],
                        )
    sudoer = BooleanField('Sudoer')
    user_name = TextField('Username', [validators.Required("You must give a username")])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords much match')])
    confirm = PasswordField('Repeat Password')
