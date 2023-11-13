from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
from flask_migrate import Migrate

def ribuan_separator(angka):
    return '{:,}'.format(int(angka)).replace(',', '.')

app.jinja_env.filters['ribuan'] = ribuan_separator

from datetime import datetime
def tanggal_convertor(tanggal):
    try:
        return datetime.strptime(str(tanggal)[0:10], '%Y-%m-%d').strftime('%d %b %Y')
    except:
        return tanggal

app.jinja_env.filters['tanggal'] = tanggal_convertor


db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "89123y4uqh9e8hdawhd8912e"

from routes.customer import *
from routes.admin import *
from routes.auth import *