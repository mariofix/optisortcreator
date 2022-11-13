from flask_admin import Admin
from svsagro.database import db
from svsagro.models import Customer, Machine, Contact
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm


admin_site = Admin(name="SVS Ops", template_mode="bootstrap4", url="/admin.site")


class CustomerAdminView(ModelView):
    form_base_class = SecureForm
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


class MachineAdminView(ModelView):
    form_base_class = SecureForm
    form_choices = {
        "type": [
            ("optisort", "Optisort"),
            ("weightline", "Weight Line"),
            ("gubbuncher", "Gub Buncher"),
        ]
    }


admin_site.add_view(CustomerAdminView(Customer, db.session, category="SVS Agro"))
admin_site.add_view(ModelView(Contact, db.session, category="SVS Agro"))
admin_site.add_view(MachineAdminView(Machine, db.session, category="Strauss"))
