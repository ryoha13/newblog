from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_migrate import Migrate


db = SQLAlchemy()
mail = Mail()
moment = Moment()
avatars = Avatars()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
