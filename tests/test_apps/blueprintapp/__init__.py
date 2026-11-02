from pboot import Pboot

app = Pboot(__name__)
app.config["DEBUG"] = True
from blueprintapp.apps.admin import admin  # noqa: E402
from blueprintapp.apps.frontend import frontend  # noqa: E402

app.register_blueprint(admin)
app.register_blueprint(frontend)
