from flask import *
import sqlite3
from flask import g

app = Flask(__name__)
app.secret_key = "secret"
DATABASE = 'database/database.db'


# from yourapplication import init_db
# init_db()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("init")


# Connexion à la base sqlite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


if __name__ == '__main__':
    print("init db")
    init_db()
    app.run()
