import os
import sqlite3

import flask
from flask import Flask, g, app
from flask_sqlalchemy import SQLAlchemy

DATABASE = f'database{os.sep}database.db'
DATABASE_TEST = f'database{os.sep}database_test.db'
db = SQLAlchemy()


# Crée un objet app et son lien avec la base de données
def create_app(test=False):
    print("dev")
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_TEST}"
        app.config['FLASK_ENV'] = "TESTING"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE}"
    db.init_app(app)
    return app


# Permet d'initialiser la base sqlite en executant le fichier SQL contenant les create table
def initdb_with_sql_file(test=False):
    # Connexion à la base sqlite
    db_app = g._database = sqlite3.connect(DATABASE if not test else DATABASE_TEST)
    db_app.row_factory = sqlite3.Row
    # Execution du contenu du fichier
    with create_app(test).open_resource('database/schema.sql', mode='r') as f:
        db_app.cursor().executescript(f.read())
    db_app.commit()
    db_app.close()
    print('Initialized the database.')


def delete_db_file(test=False):
    path = DATABASE if not test else DATABASE_TEST
    if os.path.exists(path):
        os.remove(path)
