from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache


mail = Mail()
db = SQLAlchemy()
cache = Cache()
