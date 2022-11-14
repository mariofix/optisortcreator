from svsagro.database import db
from datetime import datetime
from flask import redirect, url_for, request, current_app
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )


class CustomModelView(ModelView):
    """
    For AdminLTE3 Views
    """

    list_template = "flask-admin/model/list.html"
    create_template = "flask-admin/model/create.html"
    edit_template = "flask-admin/model/edit.html"
    details_template = "flask-admin/model/details.html"

    create_modal_template = "flask-admin/model/modals/create.html"
    edit_modal_template = "flask-admin/model/modals/edit.html"
    details_modal_template = "flask-admin/model/modals/details.html"
    extra_css = [
        "https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/4.1.5/css/flag-icons.min.css"
    ]


class SecureModelView(CustomModelView):
    """
    For Superuser related views
    """

    # We want the form token
    form_base_class = SecureForm
    page_size = 50

    def is_accessible(self):
        return (
            current_user.is_active
            and current_user.is_authenticated
            and current_user.is_superuser
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a
        view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))


class AuthModelView(CustomModelView):
    """
    For Authenticated user related views
    """

    # We want the form token
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a
        view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))
