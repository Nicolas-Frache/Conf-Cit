import MySQLdb
from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)


def connect_database(getdict=False):
    args = {"host": "localhost",
            "user": "flask",
            "host": "localhost",
            "password": "flask",
            "db": "confcit"
            }
    if getdict:
        args["cursorclass"] = MySQLdb.cursors.DictCursor
    db = MySQLdb.Connect(**args)
    return db


@app.route('/')
def home():
    return render_template("pages/home.html")


@app.route('/listeCitoyens')
def sandbox():
    try:
        with connect_database(getdict=True).cursor() as cursor:
            cursor.execute("SELECT id as 'Numéro', Prenom, Nom, Profession "
                           "from utilisateur")
            data = cursor.fetchall()
    except Exception as e:
        return render_template("pages/error.html", error=str(e))
    return render_template("pages/listeCitoyens.html", data_tab=data)


if __name__ == '__main__':
    # Extension au moteur de template qui permet de passer des paramètres dans un include
    app.jinja_env.add_extension('jinja2.ext.with')
    app.run()
