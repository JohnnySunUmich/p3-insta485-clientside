"""Views, one for each Insta485 page."""
from insta485 import app
from insta485.views.misc import misc
from insta485.views.admin import admin
from insta485.views.users import users
from insta485.views.postonly import postonly


app.register_blueprint(misc)
app.register_blueprint(admin, url_prefix='/accounts/')
app.register_blueprint(users, url_prefix='/users/')
app.register_blueprint(postonly)
