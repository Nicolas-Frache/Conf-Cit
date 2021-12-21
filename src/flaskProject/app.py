import sqlite3

from flask import *
from flask import g

# Classes relatives aux tables de la base de données pour SQLAlchemy
from model.classes import *

# Création de l'application
app = Flask(__name__)

# Connexion à la base
DATABASE = f'database{os.sep}database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Pour identifier la session de l'utilisateur actuel
app.secret_key = "secret"


# Connexion à la base sqlite pour le initdb, inutile pour le reste avec SQL Alchemy
def get_db():
    db_app = getattr(g, '_database', None)
    if db_app is None:
        db_app = g._database = sqlite3.connect(DATABASE)
        db_app.row_factory = sqlite3.Row
    return db_app


# Permet d'initialiser la base sqlite avec la commande Flask initdb
@app.cli.command('initdb')
def initdb_command():
    db_app = get_db()
    with app.open_resource('database/schema.sql', mode='r') as f:
        db_app.cursor().executescript(f.read())
    db_app.commit()
    print('Initialized the database.')


# Retourne un dictionnaire avec toute les colonnes de l'objet pour remplir un tableau plus vite
def get_all_colonnes_for_data_tab(objet):
    keys = list(vars(objet).keys())
    colonnes = {}
    for key in keys:
        if not key.startswith("_"):
            colonnes[key] = key
    return colonnes


def is_logged():
    return not request.cookies.get("username") is None


def get_header():
    header = {"is_logged": is_logged()}
    if header["is_logged"]:
        header["username"] = request.cookies.get("username")
    # TODO: prendre en compte le rôle pour un header différent
    return header


@app.route('/test/<nom>/<profession>/')
def test(nom, profession):
    user = Utilisateur(nom=nom, profession=profession)
    db.session.add(user)
    db.session.commit()
    print(request.view_args)
    return render_template("pages/home.html", header=get_header())


@app.route('/')
@app.route('/home')
def home():
    return render_template("pages/home.html", header=get_header())


@app.route('/listeCitoyens')
def lister_citoyens():
    try:
        # données: "select * from Utilisateur"
        user_list = Utilisateur.query.all()

        # Deux possibilités pour la gestion des colonnes:
        #   1 - On récupère tout et on modifie après
        # colonnes = get_all_colonnes_for_data_tab(user_list[0])

        #   2 - On crée directement ce qui nous intéresse
        colonnes = {"id": "Numéro", "nom": "Nom", "prenom": "Prénom",
                    "sexe": "Sexe", "profession": "Profession actuelle", "dateNaissance": "Date de Naissance"}
    except Exception as e:
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeCitoyens.html", data_tab=[colonnes, user_list], header=get_header())


@app.route('/nouvelleConference.html')
def creationFormulaire():
    if not is_logged():
        return render_template("pages/acessWall.html", page_title="Nouvelle Conférence", header=get_header())
    resp = make_response(render_template("pages/formulaireCreationConf.html", header=get_header()))
    return resp


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


@app.route("/nouvelleConference", methods=['GET'])
def nouvelle_conference():
    if not is_logged():
        return render_template("pages/acessWall.html", page_title="Nouvelle conférence", header=get_header())
    return render_template("pages/nouvelleConference.html", header=get_header())


@app.route("/nouvelleConference", methods=['POST'])
def nouvelle_conference_post():
    # Valeur dans le formulaire
    titre = request.form.get("titre", default="")
    theme = request.form.get("theme", default="")
    desc = request.form.get("desc", default="")
    if titre.strip() == "":
        # Erreur si le titre est vide
        flash("Le titre ne peut être vide", "error")
        return redirect(url_for("nouvelle_conference"))
    try:
        # Ajout de la conférence dans la base
        conference = Conference(titre=titre, theme=theme, description=desc)
        db.session.add(conference)
        db.session.commit()
    except Exception as e:
        return render_template("pages/error.html", error=str(e), header=get_header())
    # Message de succès et redirection vers la page de la nouvelle conférence
    flash("Conférence de citoyens crée avec succès", "sucess")
    return redirect(url_for("page_conference", idConference=conference.id))


@app.route("/conference/<int:idConference>")
def page_conference(idConference):
    # Recherche la conférence associée à l'argument et lance une 404 si elle n'existe pas (propre à flask-sqlAlchemy)
    conference = Conference.query.filter_by(id=idConference).first_or_404()
    participants = Utilisateur.query.join(Participe).filter(Participe.idConference == idConference)
    colonnes = {"id": "Numéro", "nom": "Nom", "prenom": "Prénom",
                "sexe": "Sexe", "profession": "Profession actuelle", "dateNaissance": "Date de Naissance"}
    questionnaires = conference.questionnaires
    return render_template("pages/conference.html", header=get_header(), questionnaires=questionnaires,
                           conf=conference, participants=[colonnes, participants])


@app.route("/conference")
def lister_conferences():
    # Lister toutes les conférences en cours
    try:
        # données: "select * from Conference"
        conferences = Conference.query.all()
    except Exception as e:
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeConferences.html", data_tab=conferences, header=get_header())


# Pour l'execution en ligne de commande directement avec 'Python3 app.py'
if __name__ == '__main__':
    app.run()
