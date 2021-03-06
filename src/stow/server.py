from flask import Flask
from flask_migrate import Migrate

from stow import models
from stow.config import Config
from stow.patches import register_patches
from stow.views import api, web


# Initialize main app
app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)
app.jinja_env.auto_reload = True

register_patches(app)

with app.app_context():
    # Initialize extensions
    models.bcrypt.init_app(app)
    models.db.init_app(app)
    web.login_manager.init_app(app)

    # Migrate database
    manager = Migrate(app, models.db, directory='src/migrations')

# Register API views
app.register_blueprint(api.bp, url_prefix='/api')

# Register Web views
app.register_blueprint(web.bp)
