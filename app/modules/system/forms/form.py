from flask.ext.wtf import Form
from wtforms import TextAreaField, TextField, BooleanField, validators, ValidationError
from wtforms.validators import Required
from app.modules.domain.main import Domain


class AddDomain(Form):
    domain_name = TextField('Domain Name', [validators.Required('Please enter the domain name that you wish to add')])
    vhost = TextAreaField('Domain\'s Virtual Host Configuration', default=Domain(service='httpd').getDefaultVirtualHost())
    phpini = TextAreaField('Domain\'s PHP Settings', default=Domain(service='phpini').getDefaultPhpini())
