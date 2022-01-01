import traceback
from datetime import datetime, timedelta

from faker.generator import random
from flask import *

from project import create_app, delete_db_file, initdb_with_sql_file
# Classes relatives aux tables de la base de données pour SQLAlchemy
from project.database.classes import *
from project.database.populate import populate_with_random

from project.database.utils_questionnaire import process_reponse_questionnaire

# Création de l'application
app = create_app()
# Lien avec la base de données
db = SQLAlchemy(app)

# Pour identifier la session de l'utilisateur actuel
app.secret_key = "secret"


# Permet d'initialiser la base sqlite avec la commande Flask initdb
@app.cli.command('initdb')
def initdb_command():
    delete_db_file()
    initdb_with_sql_file()
    populate_with_random(1000)


def is_logged():
    return not request.cookies.get("username") is None


def get_header():
    header = {"is_logged": is_logged()}
    if header["is_logged"]:
        header["username"] = request.cookies.get("username")
    # TODO: prendre en compte le rôle pour un header différent
    return header


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    print("test")
    return render_template("pages/home.html", header=get_header())


@app.route('/listeCitoyens', methods=['GET'])
def lister_citoyens():
    try:
        # données: "select * from Utilisateur"
        user_list = Utilisateur.query.all()
        # On renomme les colonnes qui seront affichées
        colonnes = {"id": "Numéro", "nom": "Nom", "prenom": "Prénom",
                    "sexe": "Sexe", "profession": "Profession actuelle", "dateNaissance": "Date de Naissance"}
        # Reformattage des dates de naissances utilisateurs au format français
        for user in user_list:
            dn = user.dateNaissance.split("-")
            user = Utilisateur(id=user.id, nom=user.nom, prenom=user.prenom, sexe=user.sexe,
                               profession=user.profession, dateNaissance=user.dateNaissance)
            user.dateNaissance = f"{dn[2]}/{dn[1]}/{dn[0]}"
    except Exception as e:
        print(traceback.format_exc())
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeCitoyens.html", data_tab=[colonnes, user_list], header=get_header())


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
    flash('Vous êtes maintenant connecté', 'sucess')
    resp = make_response(redirect(redirect_url))
    resp.set_cookie("username", nom)
    return resp


@app.route("/nouvelleConference", methods=['GET'])
def nouvelle_conference():
    if not is_logged():
        return render_template("pages/acessWall.html", page_title="Nouvelle conférence", header=get_header())
    nb_citoyens = Utilisateur.query.count()
    return render_template("pages/creationConference.html", nb_citoyens=nb_citoyens, header=get_header())


@app.route("/nouvelleConference", methods=['POST'])
def nouvelle_conference_post():
    nb_citoyens = Utilisateur.query.count()
    # Valeur dans le formulaire
    titre = request.form.get("titre", default="")
    theme = request.form.get("theme", default="")
    desc = request.form.get("desc", default="")
    taille_panel = request.form.get("taille_panel")
    print(taille_panel)

    if titre.strip() == "":
        # Erreur si le titre est vide
        flash("Le titre ne peut être vide", "error")
        return redirect(url_for("nouvelle_conference"))
    if not taille_panel.isnumeric() or int(taille_panel) <= 0 or int(taille_panel) > nb_citoyens:
        # Erreur si la taille du panel de citoyens n'est pas valide
        flash(f"Le taille du panel de citoyens doit être entier positif inférieur ou égale au nombre de "
              f"citoyens inscrits ({nb_citoyens})", "error")
        return redirect(url_for("nouvelle_conference"))
    try:
        # Ajout de la conférence dans la base
        conference = Conference(titre=titre, theme=theme, description=desc)
        db.session.add(conference)
        db.session.commit()

        # Ajout des n participants aléatoires sans répétitions
        listeIndexAleatoires = random.sample(range(0, nb_citoyens), int(taille_panel))
        for i in listeIndexAleatoires:
            db.session.add(Participe(idUtilisateur=Utilisateur.query[i].id,
                                     idConference=conference.id))
        db.session.commit()
    except Exception as e:
        print(traceback.format_exc())
        return render_template("pages/error.html", error=str(e), header=get_header())
    # Message de succès et redirection vers la page de la nouvelle conférence
    flash("Conférence de citoyens crée avec succès", "sucess")
    return redirect(url_for("page_conference", idConference=conference.id))


@app.route("/conference/<int:idConference>")
def page_conference(idConference):
    # Recherche la conférence associée à l'argument et lance une 404 si elle n'existe pas (propre à flask-sqlAlchemy)
    conference = Conference.query.filter_by(id=idConference).first_or_404()
    participants = Utilisateur.query.join(Participe).filter(Participe.idConference == idConference).all()
    # On associe le nom des attributs du modèle au nom des colonnes à afficher
    colonnes = {"id": "Numéro", "nom": "Nom", "prenom": "Prénom",
                "sexe": "Sexe", "profession": "Profession actuelle", "dateNaissance": "Date de Naissance"}

    questionnaires = conference.questionnaires
    # Reformattage des dates de création du format    "UTC: YYYY-MM-DD hh:mm:ss"
    #                                               à "UTC+1: DD/MM/YYYY hh:mm"
    for questionnaire in questionnaires:
        datetime_object = datetime.strptime(questionnaire.dateFermeture, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
        questionnaire.dateFermeture = datetime_object.strftime("%d/%m/%Y %H:%M")
    return render_template("pages/conference.html", header=get_header(), questionnaires=questionnaires,
                           conf=conference, participants=[colonnes, participants])


@app.route("/conference")
def lister_conferences():
    # Lister toutes les conférences en cours
    try:
        # données: "select * from Conference"
        conferences = Conference.query.all()
    except Exception as e:
        print(traceback.format_exc())
        return render_template("pages/error.html", error=str(e), header=get_header())
    return render_template("pages/listeConferences.html", data_tab=conferences, header=get_header())


@app.route("/nouveauQuestionnaire/<int:idConference>", methods=['GET'])
def nouveau_questionnaire(idConference):
    if Conference.query.filter_by(id=idConference).count() == 0:
        erreur = "L'accès à la page de création de questionnaire se fait en cliquant sur le bouton correspondant " \
                 "sur la page de la conférence de citoyens associée (url de type /conference/<idConference>)"
        return render_template("pages/error.html", error=erreur, header=get_header())
    conference = Conference.query.filter_by(id=idConference).first()
    return render_template("pages/creationQuestionnaire.html", header=get_header(), conference=conference)


@app.route("/nouveauQuestionnaire", methods=['POST'])
def nouveau_questionnaire_post():
    try:
        # Construction des objets de base de données correspondants aux résultat du form
        form = request.form
        # Cas d'erreur si la conférence correspondante n'est pas valide
        if Conference.query.filter_by(id=form["id_conf"]).count() == 0:
            raise Exception()
        # Création du questionnaire (on le commit directement car on a besoin de l'id généré après)
        questionnaire: Questionnaire = Questionnaire(titre=form["titre_questionnaire"],
                                                     idConference=form["id_conf"])
        db.session.add(questionnaire)
        db.session.commit()
        # Création des questions (qu'on commit à chaque fois pour la même raison)
        for idxQuestion in range(1, int(form["nb_questions"]) + 1):
            contenu = form[f"q_{idxQuestion}"]
            typeQ = "TEXTE" if (int(form[f"radio_{idxQuestion}"]) == 1) else "QCM"
            question: Question = Question(numero=idxQuestion,
                                          typeQuestion=typeQ,
                                          contenu=contenu,
                                          idQuestionnaire=questionnaire.id)
            db.session.add(question)
            db.session.commit()
            if typeQ == "QCM":
                # Si c'est un QCM, création de tous les objets ChoixQcm nécessaires
                for idxChoix in range(1, int(form[f"nb_choix_qcm_{idxQuestion}"]) + 1):
                    choix_qcm: ChoixQcm = ChoixQcm(numero=idxChoix,
                                                   contenu=form[f"qcm-{idxQuestion}-{idxChoix}"],
                                                   idQuestion=question.id)
                    db.session.add(choix_qcm)
                db.session.commit()
    except Exception:
        print(traceback.format_exc())
        return render_template("pages/error.html", error="Le contenu du formulaire est mal construit",
                               header=get_header())
    flash("Questionnaire crée avec succès", "sucess")
    return redirect(url_for("page_conference", idConference=int(form["id_conf"])))


@app.route("/conference/questionnaire/<idQuestionnaire>")
def afficher_questionnaire(idQuestionnaire):
    # Affiche le contenu du questionnaire d'identifiant idQuestionnaire
    try:
        questionnaire = Questionnaire.query.filter(Questionnaire.id == idQuestionnaire).all()[0]
        conference = Conference.query.filter(questionnaire.idConference == Conference.id).all()[0]
        questions = Question.query.filter(Question.idQuestionnaire == idQuestionnaire)
        participants = Utilisateur.query.join(Participe).filter(Participe.idConference == conference.id).all()
        print(participants)
    except Exception as e:
        print(traceback.format_exc())
        return render_template("pages/error.html", error=str(e), header=get_header())
    colonnes = {"id": "Numéro", "nom": "Nom", "prenom": "Prénom",
                "sexe": "Sexe", "profession": "Profession actuelle", "dateNaissance": "Date de Naissance"}
    return render_template('pages/questionnaire.html', header=get_header(), quest=questionnaire, conf=conference,
                           qu=questions, part=[colonnes, participants])


@app.route("/resultat/<idQuestionnaire>")
def resultats(idQuestionnaire):
    questions = Question.query.filter(Question.idQuestionnaire == idQuestionnaire).all()
    res = []
    for q in questions:
        if q.typeQuestion == "TEXTE":
            res.append((q, ()))
        else:
            tuplesQcm = []
            for choixQcm in q.liste_choix_qcm:
                nbReponse = len(choixQcm.reponses_qcm)
                tuplesQcm.append((choixQcm, nbReponse))
            res.append((q, tuplesQcm))
    return render_template("pages/resultats.html", header=get_header(), id=idQuestionnaire, donnees=res)


@app.route("/repondre/<int:idquestionnaire>", methods=['GET'])
def repondre_questionnaire(idquestionnaire):
    # Erreur 404 si le questionnaire n'existe pas
    questionnaire = Questionnaire.query.filter_by(id=idquestionnaire).first_or_404()
    # On construit une liste de tuple de (Question, ChoixQCM)
    questions = Question.query.filter_by(idQuestionnaire=idquestionnaire).order_by(Question.numero).all()
    # TODO utiliser l'id de l'utilisateur connecté
    id_utilisateur = 1
    return render_template("pages/reponseQuestionnaire.html", header=get_header(), questions=questions,
                           questionnaire=questionnaire, id_utilisateur=id_utilisateur)


@app.route("/repondre", methods=['POST'])
def repondre_questionnaire_post():
    try:
        process_reponse_questionnaire(request.form)
    except Exception as error:
        print(traceback.format_exc())
        db.session.rollback()
        return render_template("pages/error.html", error=error.value.args[0],
                               header=get_header())
    flash("Réponses au questionnaire soumises avec succès", "sucess")
    idConf = Questionnaire.query.filter_by(id=request.form["id_questionnaire"]).first().idConference
    return redirect(url_for("page_conference", idConference=int(idConf)))


# Pour l'execution en ligne de commande directement avec 'Python3 app.py'
if __name__ == '__main__':
    app.run()
