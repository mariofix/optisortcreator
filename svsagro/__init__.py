from flask import Flask, session, request, url_for
from svsagro.database import db, migrations
from svsagro.admin import admin_site
from svsagro.models import User, Role
from svsagro.mail import mail
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask_adminlte3 import AdminLTE3


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"instance.{app.config['ENV']}")
    app.config.from_prefixed_env()

    toolbar = DebugToolbarExtension(app)
    babel = Babel(app)
    adminlte = AdminLTE3(app)

    db.init_app(app)
    migrations.init_app(app, db, render_as_batch=True)
    admin_site.init_app(app)
    mail.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @babel.localeselector
    def get_locale():
        if request.args.get("lang"):
            session["lang"] = request.args.get("lang")
        return session.get("lang", app.config.get("BABEL_DEFAULT_LOCALE"))

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, "user", None)
        return user.timezone or app.config.get("BABEL_DEFAULT_TIMEZONE")

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin_site.base_template,
            admin_view=admin_site.index_view,
            h=admin_helpers,
            get_url=url_for,
            app=app,
        )

    @app.get("/")
    def home():
        app.logger.info("home")
        return "<html><body>/</body></html>"

    return app


the_app = create_app()
