from flask import Flask, render_template
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.views.authors import authors_app
from blog.admin import admin
from blog.api import init_api


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    flask_bcrypt.init_app(app)
    admin.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(articles_app, url_prefix="/articles")
    app.register_blueprint(auth_app, url_prefix="/auth")
    app.register_blueprint(authors_app, url_prefix="/authors")


app = Flask(__name__)
cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
API_URL = os.environ.get("API_URL")
app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db, compare_type=True)
init_extensions(app)
register_blueprints(app)
api = init_api(app)


@app.route("/")
def index():
    return render_template("index.html")
