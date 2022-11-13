from flask import Flask, session, request
from svsagro.database import db, migrations
from svsagro.admin import admin_site
from flask_babelex import Babel


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"instance.{app.config['ENV']}")
    app.config.from_prefixed_env()

    babel = Babel(app)
    db.init_app(app)
    migrations.init_app(app, db, render_as_batch=True)
    admin_site.init_app(app)

    @babel.localeselector
    def get_locale():
        if request.args.get("lang"):
            session["lang"] = request.args.get("lang")
        return session.get("lang", "en")

    return app
