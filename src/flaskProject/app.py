from flask import *
import sqlite3
from flask import g

app = Flask(__name__)
app.secret_key = "secret"
DATABASE = 'database/database.db'


# Connexion à la base sqlite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# function that combines getting the cursor, executing and fetching the results
# see: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
        user_list = query_db("SELECT *"
                             "from UTILISATEUR")
    # user_list = query_db("SELECT id as 'Numéro', Prenom, Nom, Profession, DATENAISSANCE as 'date'"
    #                     "from UTILISATEUR")
    except Exception as e:
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeCitoyens.html", data_tab=user_list, header=get_header())




# Page pour faire des tests
@app.route('/sandbox')
def sandbox():
    if not is_logged():
        return render_template("pages/acessWall.html", page_title="Sandbox", header=get_header())
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


# Pour l'execution en ligne de commande directement avec 'Python3 app.py'
if __name__ == '__main__':
    app.run()
