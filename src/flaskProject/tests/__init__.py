import os

from flask_sqlalchemy import SQLAlchemy
from project import create_app as parent_create_app


def create_app():
    print("************ Creation of test app ************")
    app_tmp = parent_create_app(test=True)
    return app_tmp


app_test = create_app()
app_test.app_context().push()
db = SQLAlchemy(app_test)
