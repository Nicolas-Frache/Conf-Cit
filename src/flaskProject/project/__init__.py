import os
import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DATABASE = f'database{os.sep}database.db'
DATABASE_TEST = f'database{os.sep}database_test.db'
db = SQLAlchemy()


# Crée un objet app et son lien avec la base de données
def create_app(test=False):
    print("dev")
    app_tmp = Flask(__name__, template_folder="templates", static_folder="static")
    app_tmp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test:
        app_tmp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_TEST}"
        app_tmp.config['FLASK_ENV'] = "TESTING"
    else:
        app_tmp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE}"
    db.init_app(app_tmp)
    return app_tmp


# Permet d'initialiser la base sqlite en executant le fichier SQL contenant les create table
def initdb_with_sql_file(test=False):
    # Connexion à la base sqlite
    path = os.path.join('project', DATABASE if not test else DATABASE_TEST)
    db_app = sqlite3.connect(path)
    db_app.row_factory = sqlite3.Row
    # Execution du contenu du fichier
    with create_app(test).open_resource(f'database{os.sep}schema.sql', mode='r') as f:
        db_app.cursor().executescript(f.read())
    db_app.commit()
    db_app.close()
    print('Database initialized')


def delete_db_file(test=False):
    path = os.path.join('project', DATABASE if not test else DATABASE_TEST)
    if os.path.exists(path):
        os.remove(path)
