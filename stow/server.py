from flask import Flask

import stow.models as models
import stow.views as views
from .config import Config


# Initialize main app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../stow.db'

with app.app_context():
    # Initialize extensions
    models.bcrypt.init_app(app)
    models.db.init_app(app)

    # Initialize database
    models.db.create_all()
    models.db.session.commit()


# Register views
app.register_error_handler(Exception, views.error_handler)
views.TokenView.register(app, strict_slashes=False)
views.UserView.register(app, strict_slashes=False)
views.StowView.register(app, strict_slashes=False)
