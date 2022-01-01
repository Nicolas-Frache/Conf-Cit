from project.database.classes import *
from flask_sqlalchemy import SQLAlchemy


def process_reponse_questionnaire(form):
    """
    A partir d'une réponse de questionnaire, teste la validité de l'ensemble des facteurs
    et ajoute à la base de données l'ensemble des réponses au questionnaire
    :param form: Dictionnaire qui représente la réponse au questionnaire
    :raise: Exception("message") - En cas de non validité d'un des paramètres
    """
    try:
        error = "Le contenu du formulaire est mal construit"
        # Vérifications de l'acceptabilité de la réponse avant de commencer
        # Existence de l'utilisateur
        if Utilisateur.query.filter_by(id=form["id_utilisateur"]).count() == 0:
            raise Exception("Pas d'utilisateur valide associé à cette réponse", "E001")
        # Existence du questionnaire
        if Questionnaire.query.filter_by(id=form["id_questionnaire"]).count() == 0:
            raise Exception("Pas de questionnaire valide associé à cette réponse", "E002")
        # Participation de l'utilisateur à la conférence de citoyens associée au questionnaire
        utilisateur = Utilisateur.query.filter_by(id=form["id_utilisateur"]).first()
        questionnaire = Questionnaire.query.filter_by(id=form["id_questionnaire"]).first()
        conference = Conference.query.filter_by(id=questionnaire.idConference).first()
        if Participe.query.filter_by(idUtilisateur=utilisateur.id, idConference=conference.id).count() == 0:
            raise Exception(
                f"Pour pouvoir répondre à ce questionnaire il faut participer à la conférence {conference.titre}", "E003")
        # Vérification que l'utilisateur n'a pas déjà répondu au questionnaire
        premiere_question: Question = questionnaire.questions[0]
        if ReponseTexte.query.filter_by(idQuestion=premiere_question.id, idUtilisateur=utilisateur.id).count() \
                + ReponseQcm.query.filter_by(idQuestion=premiere_question.id, idUtilisateur=utilisateur.id).count() != 0:
            raise Exception("Un utilisateur ne peut répondre qu'une fois à un questionnaire", "E004")

        # Parcours des questions pour enregistrer les réponses dans la base
        object_to_add = []
        for question in questionnaire.questions:
            if question.typeQuestion == "TEXTE":
                reponse = ReponseTexte(contenu=form[f"texte_{question.id}"],
                                       idQuestion=question.id,
                                       idUtilisateur=utilisateur.id)
            else:
                # Vérification de la validité du choixQcm
                if ChoixQcm.query.filter_by(id=form[f"q_{question.id}"]).count() == 0:
                    raise Exception("Réponse QCM inexistante", "E005")
                if ChoixQcm.query.filter_by(id=form[f"q_{question.id}"]).first().idQuestion != question.id:
                    raise Exception("Incohérence entre la réponse et la question", "E006")

                reponse = ReponseQcm(idChoix=form[f"q_{question.id}"],
                                     idQuestion=question.id,
                                     idUtilisateur=utilisateur.id)
            object_to_add.append(reponse)
        for obj in object_to_add:
            db.session.add(obj)
        db.session.commit()
    except KeyError:
        raise Exception("Le contenu du formulaire est mal construit", "E000")
