from flask_admin import Admin, expose, AdminIndexView, form
from flask_admin.base import MenuLink
from flask_admin.actions import action
from svsagro.database import db
from svsagro.models import Customer, Machine, Contact, User, Role, Document
from svsagro.mixins import SecureModelView, AuthModelView
from flask_security import hash_password
from wtforms.fields import PasswordField
from slugify import slugify
from flask_babel import lazy_gettext as _


class MyAdminIndexView(AdminIndexView):
    extra_css = [
        "https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/4.1.5/css/flag-icons.min.css"
    ]

    @expose("/", methods=["GET", "POST"])
    def index(self):
        return self.render("myadmin3/my_index.html")


admin_site = Admin(
    name="SVSOps",
    template_mode="bootstrap4",
    url="/admin.site",
    base_template="myadmin3/my_master.html",
    index_view=MyAdminIndexView(url="/admin.site"),
    endpoint="admin",
)
admin_site.add_link(MenuLink(name=_("Logout"), url="/logout"))


class CustomerAdminView(SecureModelView):
    form_choices = {
        "country": [
            ("CL", "Chile"),
            ("PE", "Peru"),
            ("EC", "Ecuador"),
            ("MX", "Mexico"),
            ("US", "USA"),
            ("CA", "Canada"),
        ]
    }
    column_list = ["name", "country"]
    can_view_details = True


class MachineAdminView(AuthModelView):
    form_choices = {
        "type": [
            ("Optisort", "Optisort"),
            ("WeightLine", "Weight Line"),
            ("GubBuncher", "Gub Buncher"),
        ],
        "direction": [
            ("Left", "Left"),
            ("Right", "Right"),
        ],
    }
    column_list = [
        "number",
        "type",
        "model",
        "customer",
        "direction",
        "instalation_date",
    ]
    can_view_details = True


class ContactAdminView(SecureModelView):
    column_list = ["name", "email", "customer"]
    can_view_details = True


class UserAdminView(SecureModelView):
    form_excluded_columns = ["password"]
    column_list = ["username", "email", "active", "staff", "roles"]
    can_view_details = True

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password2 = PasswordField(_("New Password"))
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = hash_password(model.password2)


class RoleAdminView(SecureModelView):
    column_list = ["name", "slug", "description", "created_at"]

    def on_model_change(self, form, model, is_created):
        if is_created and not model.slug:
            model.slug = slugify(model.name)


class DocumentAdminView(SecureModelView):
    column_list = ["name", "category", "machine"]
    form_overrides = {"path": form.FileUploadField}
    form_args = {
        "path": {
            "label": _("File"),
            "base_path": "svsagro/static/documents/",
            "allow_overwrite": True,
        }
    }
    form_choices = {
        "category": [
            ("Optisort", "Optisort"),
            ("WeightLine", "Weight Line"),
            ("GubBuncher", "Gub Buncher"),
        ]
    }
    can_view_details = True
    column_filters = ["machine", "category"]
    create_modal = True
    edit_modal = True
    column_exclude_list = ["created_at", "updated_at"]
    form_excluded_columns = ["updated_at"]


admin_site.add_view(CustomerAdminView(Customer, db.session, category="SVS Agro"))
admin_site.add_view(UserAdminView(User, db.session, category=_("Security")))
admin_site.add_view(RoleAdminView(Role, db.session, category=_("Security")))
admin_site.add_view(ContactAdminView(Contact, db.session, category="SVS Agro"))
admin_site.add_view(MachineAdminView(Machine, db.session, category="Strauss"))
admin_site.add_view(DocumentAdminView(Document, db.session, category="Strauss"))
