from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_ckeditor import CKEditor


db = SQLAlchemy()
mail = Mail()
moment = Moment()
avatars = Avatars()
migrate = Migrate()
bootstrap = Bootstrap()
dropzone = Dropzone()
whooshee = Whooshee()
csrf = CSRFProtect()
toolbar = DebugToolbarExtension()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
