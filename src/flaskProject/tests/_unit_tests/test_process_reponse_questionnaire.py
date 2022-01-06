import pytest
from project.database.utils_questionnaire import process_reponse_questionnaire
from project.database.classes import *


@pytest.fixture(autouse=True)
def donnees_test():
    """
    Crée et insère dans la base des données de test automatiquement à chaque début de test
    """
    db.session.close()
    # Création questionnaires
    # 1 - complet
    db.session.add(Conference(id=1))
    db.session.add(Questionnaire(id=1, idConference=1))
    db.session.add(Question(id=1, numero=1, idQuestionnaire=1, typeQuestion="TEXTE"))
    db.session.add(Question(id=2, numero=2, idQuestionnaire=1, typeQuestion="QCM"))
    db.session.add(Question(id=3, numero=3, idQuestionnaire=1, typeQuestion="TEXTE"))

    db.session.add(ChoixQcm(id=1, numero=1, idQuestion=2))
    db.session.add(ChoixQcm(id=2, numero=2, idQuestion=2))
    db.session.add(ChoixQcm(id=3, numero=3, idQuestion=2))

    # 2 - Une seule question QCM
    db.session.add(Questionnaire(id=2, idConference=1))
    db.session.add(Question(id=4, numero=1, idQuestionnaire=2, typeQuestion="QCM"))
    db.session.add(ChoixQcm(id=4, numero=1, idQuestion=4))

    # Utilisateur participant
    db.session.add(Utilisateur(id=1))
    db.session.add(Participe(idUtilisateur=1, idConference=1))

    # Utilisateur ne participant pas
    db.session.add(Utilisateur(id=2))

    # Utilisateur ayant déjà répondu
    db.session.add(Utilisateur(id=3))
    db.session.add(Participe(idUtilisateur=3, idConference=1))
    db.session.add(ReponseTexte(id=1, idUtilisateur=3, idQuestion=1))
    db.session.add(ReponseQcm(idChoix=2, idUtilisateur=3, idQuestion=2))
    db.session.add(ReponseTexte(id=2, idUtilisateur=3, idQuestion=3))

    db.session.commit()


def test_process_reponse_questionnaire_avec_utilisateur_inexistant():
    """
    AVEC un id d'utilisateur inexistant
    QUAND on appelle process_reponse_questionnaire avec cet utilisateur dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_utilisateur": 10, "id_questionnaire": 1})
    assert exception.value.args[1] == "E001"


def test_process_reponse_questionnaire_avec_questionnaire_inexistant():
    """
    AVEC un id de conférence inexistant
    QUAND on appelle process_reponse_questionnaire avec cette conférence dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_utilisateur": 1, "id_questionnaire": 10})
    assert exception.value.args[1] == "E002"


def test_process_reponse_questionnaire_avec_utilisateur_non_participant():
    """
    AVEC un id d'utilisateur existant mais ne participant pas à la conférence de citoyens
    QUAND on appelle process_reponse_questionnaire avec cet utilisateur dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_utilisateur": 2, "id_questionnaire": 1})
    assert exception.value.args[1] == "E003"


def test_process_reponse_questionnaire_avec_utilisateur_ayant_deja_repondu():
    """
    AVEC un id d'utilisateur existant ayant déja répondu au questionnaire
    QUAND on appelle process_reponse_questionnaire avec cet utilisateur dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_utilisateur": 3, "id_questionnaire": 1})
    assert exception.value.args[1] == "E004"


def test_process_reponse_questionnaire_formulaire_mal_construit_donnees_manquantes():
    """
    AVEC un des données d'entrées insuffisantes (champs manquant)
    QUAND on appelle process_reponse_questionnaire avec cet utilisateur dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({})
    assert exception.value.args[1] == "E000"

    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_utilisateur": 1})
    assert exception.value.args[1] == "E000"

    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1})
        assert exception.value.args[1] == "E000"

    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                       "texte_2": "r2", "texte_3": "r3"})
        assert exception.value.args[1] == "E000"

    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                       "texte_42": "r2", "texte_3": "r3"})
        assert exception.value.args[1] == "E000"


def test_process_reponse_questionnaire_formulaire_choixqcm_inexistant():
    """
    AVEC une réponse correspondant à un choix de QCM inexistant
    QUAND on appelle process_reponse_questionnaire avec ces données d'entrées
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                       "q_2": 42, "texte_3": "r3"})
    assert exception.value.args[1] == "E005"

    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                       "q_2": "texte_au_lieu_d_un_id", "texte_3": "r3"})
    assert exception.value.args[1] == "E005"


def test_process_reponse_questionnaire_formulaire_incoherence_choixqcm():
    """
    AVEC une réponse correspondant à un choix de QCM d'une autre question
    QUAND on appelle process_reponse_questionnaire avec ces données d'entrées
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                       "q_2": 4, "texte_3": "r3"})
    assert exception.value.args[1] == "E006"


def test_process_reponse_questionnaire_valide():
    """
    AVEC une réponse valide
    QUAND on appelle process_reponse_questionnaire avec ces données d'entrées
    ALORS on vérifie que l'erreur associée est lancée
    """
    process_reponse_questionnaire({"id_questionnaire": 1, "id_utilisateur": 1, "texte_1": "r1",
                                   "q_2": 2, "texte_3": "r3"})
    assert ReponseTexte.query.filter_by(idQuestion="1", idUtilisateur="1").first().contenu == "r1"
    assert ReponseTexte.query.filter_by(idQuestion="3", idUtilisateur="1").first().contenu == "r3"
    assert ReponseQcm.query.filter_by(idQuestion="2", idUtilisateur="1", idChoix=2).count() == 1
