import os

from .. import create_app as parent_create_app
from ..model.classes import *


def create_app():
    print("************ Creation of test app ************")
    app_test = parent_create_app(test=True)
    return app_test


app = create_app()
app.app_context().push()
db = SQLAlchemy(app)
