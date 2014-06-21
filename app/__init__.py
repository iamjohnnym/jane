from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
import jinja2


theme = 'sb-admin'
app = Flask(__name__)
template_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(['app/modules',
                                     'app/templates',
                                     'app/themes']),
            ])
app.jinja_loader = template_loader
assets = Environment(app)
css_all = Bundle('css/bootstrap.css')
assets.register('css_all', css_all)

app.debug = True
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
