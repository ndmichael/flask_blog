from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_alembic import Alembic


app = Flask(__name__)
app.config['SECRET_KEY'] = '6ibKMJFyt-p5Ds52qy2Jhg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# alembic = Alembic()
# alembic.init_app(app)

with app.app_context():
    from fblog.models import User, Post
    # alembic.upgrade()
    db.create_all()

from fblog import routes