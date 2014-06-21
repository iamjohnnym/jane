from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, BooleanField, validators, ValidationError
from wtforms.validators import Required

class Client(Form):
    name = TextField('Name', [validators.Required('Please Enter Your Name')])
    account_number = TextField('Account Number', [validators.Required('Please Enter Your Account Number')])
    message = TextAreaField('messages')
    

