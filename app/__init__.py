# coding:utf8
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from flask_babel import Babel, gettext as _

basedir = path.abspath(path.dirname(__file__))
bootstrap = Bootstrap()
db = SQLAlchemy()
babel = Babel()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.secret_key = 'hard to guess string'
    app.config.from_object('babel')
    app.config['BAbel_DEFAULT_LOCAL'] = 'zh'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    babel.init_app(app)
    Gravatar(app, size=64)

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app
