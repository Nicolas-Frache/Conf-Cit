import MySQLdb
from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secret"


def connect_database(getdict=False):
    args = {"host": "localhost",
            "user": "flask",
            "password": "flask",
            "db": "confcit"
            }
    if getdict:
        args["cursorclass"] = MySQLdb.cursors.DictCursor
    db = MySQLdb.Connect(**args)
    return db


def is_logged():
    return not request.cookies.get("username") is None


def get_header():
    header = {"is_logged": is_logged()}
    if header["is_logged"]:
        header["username"] = request.cookies.get("username")
    # TODO: prendre en compte le rôle pour un header différent
    return header


@app.route('/')
def home():
    return render_template("pages/home.html", header=get_header())


@app.route('/listeCitoyens')
def lister_citoyens():
    try:
        with connect_database(getdict=True).cursor() as cursor:
            cursor.execute("SELECT id as 'Numéro', Prenom, Nom, Profession "
                           "from utilisateur")
            data = cursor.fetchall()
    except Exception as e:
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeCitoyens.html", data_tab=data, header=get_header())


# Page pour faire des tests
@app.route('/sandbox')
def sandbox():
    compteur = request.cookies.get("compteur")
    if compteur is None:
        val = "0"
    else:
        val = int(compteur) + 1
    resp = make_response(render_template("pages/sandbox.html", compteur=compteur, header=get_header()))
    resp.set_cookie("compteur", str(val))
    return resp


@app.route("/deconnexion")
def se_deconnecter():
    newUrl = request.args.get("redirect", default="/")
    resp = make_response(redirect(newUrl))
    resp.set_cookie('username', '', expires=0)
    return resp


@app.route("/connexion", methods=['GET'])
def se_connecter_get():
    args = {}
    redirect_url = request.args.get("redirect", default="/")
    print(redirect_url)
    if is_logged():
        args["error"] = "Vous devez d'abord vous déconnecter pour réaliser cette action"
        args["is_disabled"] = True
    return render_template("pages/seConnecter.html", header=get_header(), redirect=redirect_url, **args)


@app.route("/connexion", methods=['POST'])
def se_connecter_post():
    nom = request.form.get("nom", default="").strip()
    mdp = request.form.get("mdp", default="")
    redirect_url = request.args.get("redirect", default="/")
    if nom == "" or mdp == "":
        return render_template("pages/seConnecter.html",
                               header=get_header(),
                               error="Erreur lors de la saisie des identifiants",
                               redirect=redirect_url)

    flash('Vous êtes maintenant connecté')
    resp = make_response(redirect(redirect_url))
    resp.set_cookie("username", nom)
    return resp


if __name__ == '__main__':
    # Extension au moteur de template qui permet de passer des paramètres dans un include
    app.jinja_env.add_extension('jinja2.ext.with')
    app.run()
