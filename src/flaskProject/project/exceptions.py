def formulaireMalConstruitError():
    raise Exception("Le contenu du formulaire est mal construit", "E000")


def utilisateurInexistantError():
    raise Exception("Pas d'utilisateur valide associé à cette réponse", "E001")


def questionnaireDansReponseNonValideError():
    raise Exception("Pas de questionnaire valide associé à cette réponse", "E002")


def reponseSansParticipationError(confTitre):
    raise Exception(
        f"Pour pouvoir répondre à ce questionnaire il faut participer à la conférence {confTitre}",
        "E003")


def utilsateurAyenDejaReponduError():
    raise Exception("Un utilisateur ne peut répondre qu'une fois à un questionnaire", "E004")


def choixDeQcmInexistantError():
    raise Exception("Réponse QCM inexistante", "E005")


def reponseIncoherenteError():
    raise Exception("Incohérence entre la réponse et la question", "E006")


def conferenceInexistanteError():
    raise Exception("La conférence liée à ce questionnaire n'existe pas", "E007")


def nombreChoixQcmInsuffisantError():
    raise Exception("Il faut au moins deux choix de réponse pour une question QCM", "E008")


