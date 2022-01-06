from project.database.classes import *
from flask_sqlalchemy import SQLAlchemy

from project.exceptions import *


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
            utilisateurInexistantError()
        # Existence du questionnaire
        if Questionnaire.query.filter_by(id=form["id_questionnaire"]).count() == 0:
            questionnaireDansReponseNonValideError()
        # Participation de l'utilisateur à la conférence de citoyens associée au questionnaire
        utilisateur = Utilisateur.query.filter_by(id=form["id_utilisateur"]).first()
        questionnaire = Questionnaire.query.filter_by(id=form["id_questionnaire"]).first()
        conference = Conference.query.filter_by(id=questionnaire.idConference).first()
        if Participe.query.filter_by(idUtilisateur=utilisateur.id, idConference=conference.id).count() == 0:
            reponseSansParticipationError(conference.titre)
        # Vérification que l'utilisateur n'a pas déjà répondu au questionnaire
        premiere_question: Question = questionnaire.questions[0]
        if ReponseTexte.query.filter_by(idQuestion=premiere_question.id, idUtilisateur=utilisateur.id).count() \
                + ReponseQcm.query.filter_by(idQuestion=premiere_question.id,
                                             idUtilisateur=utilisateur.id).count() != 0:
            utilsateurAyenDejaReponduError()
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
                    choixDeQcmInexistantError()
                if ChoixQcm.query.filter_by(id=form[f"q_{question.id}"]).first().idQuestion != question.id:
                    reponseIncoherenteError()
                reponse = ReponseQcm(idChoix=form[f"q_{question.id}"],
                                     idQuestion=question.id,
                                     idUtilisateur=utilisateur.id)
            object_to_add.append(reponse)
        for obj in object_to_add:
            db.session.add(obj)
        db.session.commit()
    except KeyError:
        formulaireMalConstruitError()


def process_creation_questionnaire_data(form):
    try:
        # Cas d'erreur si la conférence correspondante n'est pas valide
        if Conference.query.filter_by(id=form["id_conf"]).count() == 0:
            conferenceInexistanteError()
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
                if int(form[f"nb_choix_qcm_{idxQuestion}"]) < 2:
                    nombreChoixQcmInsuffisantError()
                # Si c'est un QCM, création de tous les objets ChoixQcm nécessaires
                for idxChoix in range(1, int(form[f"nb_choix_qcm_{idxQuestion}"]) + 1):
                    choix_qcm: ChoixQcm = ChoixQcm(numero=idxChoix,
                                                   contenu=form[f"qcm-{idxQuestion}-{idxChoix}"],
                                                   idQuestion=question.id)
                    db.session.add(choix_qcm)
                db.session.commit()
    except KeyError:
        formulaireMalConstruitError()
