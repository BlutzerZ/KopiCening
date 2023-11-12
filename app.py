from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "89123y4uqh9e8hdawhd8912e"

from routes.customer import *
from routes.admin import *
from routes.auth import *