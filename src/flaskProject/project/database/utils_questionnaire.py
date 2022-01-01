from project.database.classes import *
from flask_sqlalchemy import SQLAlchemy


def process_reponse_questionnaire(form):
    """
    A partir d'une réponse de questionnaire, teste la validité de l'ensemble des facteurs
    et ajoute à la base de données l'ensemble des réponses au questionnaire
    :param form: Dictionnaire qui représente la réponse au questionnaire
    :raise: Exception("message") - En cas de non validité d'un des paramètres
    """
    error = "Le contenu du formulaire est mal construit"
    # Vérifications de l'acceptabilité de la réponse avant de commencer
    # Existence de l'utilisateur
    if Utilisateur.query.filter_by(id=form["id_utilisateur"]).count() == 0:
        raise Exception("Pas d'utilisateur valide associé à cette réponse")
    # Existence du questionnaire
    if Questionnaire.query.filter_by(id=form["id_questionnaire"]).count() == 0:
        raise Exception("Pas de questionnaire valide associé à cette réponse")
    # Participation de l'utilisateur à la conférence de citoyens associée au questionnaire
    utilisateur = Utilisateur.query.filter_by(id=form["id_utilisateur"]).first()
    questionnaire = Questionnaire.query.filter_by(id=form["id_questionnaire"]).first()
    conference = Conference.query.filter_by(id=questionnaire.idConference).first()
    if Participe.query.filter_by(idUtilisateur=utilisateur.id, idConference=conference.id).count() == 0:
        raise Exception(
            "Pour pouvoir répondre à ce questionnaire il faut participer à la conférence " + conference.titre)
    # Vérification que l'utilisateur n'a pas déjà répondu au questionnaire
    premiere_question: Question = questionnaire.questions[0]
    if ReponseTexte.query.filter_by(idQuestion=premiere_question.id, idUtilisateur=utilisateur.id).count() \
            + ReponseQcm.query.filter_by(idQuestion=premiere_question.id, idUtilisateur=utilisateur.id).count() != 0:
        raise Exception("Un utilisateur ne peut répondre qu'une fois à un questionnaire")

    # Parcours des questions pour enregistrer les réponses dans la base
    for question in questionnaire.questions:
        if question.typeQuestion == "TEXTE":
            reponse = ReponseTexte(contenu=form[f"texte_{question.id}"],
                                   idQuestion=question.id,
                                   idUtilisateur=utilisateur.id)
        else:
            reponse = ReponseQcm(idChoix=form[f"q_{question.id}"],
                                 idQuestion=question.id,
                                 idUtilisateur=utilisateur.id)
        db.session.add(reponse)
    db.session.commit()
