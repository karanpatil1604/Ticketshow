from flask import current_app as app

from app_user import auth as user_auth
from app_show_manager import routes
from app_admin import auth as admin_auth
from app_admin import crud as admin_crud

app.register_blueprint(routes.bp)
app.register_blueprint(admin_auth.bp)
app.register_blueprint(user_auth.bp)
app.register_blueprint(admin_crud.bp)

from app_admin.endpoints import *