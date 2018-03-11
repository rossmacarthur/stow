from flask import Flask

import stow.models as models
from stow.views import api, web
from stow.config import Config
from stow.patches import register_patches

# Initialize main app
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../stow.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True

register_patches(app)

with app.app_context():
    # Initialize extensions
    models.bcrypt.init_app(app)
    models.db.init_app(app)
    web.login_manager.init_app(app)

    # Initialize database
    models.db.create_all()
    models.db.session.commit()

# Register API views
app.register_blueprint(api.bp, url_prefix='/api')

# Register Web views
app.register_blueprint(web.bp)
