import pytest
from project.database.utils_questionnaire import *
from project.database.classes import *


def test_process_creation_questionnaire_avec_conference_inexistante():
    """
    AVEC un id de conference inexistant
    QUAND on appelle process_creation_questionnaire_data avec cette conference dans le formulaire
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        process_creation_questionnaire_data({"id_conf": 1})
    assert exception.value.args[1] == "E007"


def test_process_creation_questionnaire_avec_nombre_insuffisant_de_choix_qcm():
    """
    AVEC une question QCM n'ayant qu'une réponse possible
    QUAND on appelle process_creation_questionnaire_data avec cette question
    ALORS on vérifie que l'erreur associée est lancée
    """
    with pytest.raises(Exception) as exception:
        # Creation conférence
        db.session.close()
        db.session.add(Conference(id=1))
        db.session.commit()

        process_creation_questionnaire_data(
            {"id_conf": 1, "titre_questionnaire": "titre", "nb_questions": 1, "q_1": "contenu",
             "radio_1": 0, "nb_choix_qcm_1": 1, "qcm-1-1": "choix 1"})
        assert exception.value.args[1] == "E008"


def test_process_creation_questionnaire_valide():
    """
     AVEC un formulaire de creation valide
     QUAND on appelle process_creation_questionnaire_data avec ce formulaire
     ALORS on vérifie que le questionnaire et les questions existent bien dans la base de données
     """
    # Creation conférence
    db.session.close()
    db.session.add(Conference(id=1))
    db.session.commit()

    process_creation_questionnaire_data({"id_conf": 1, "titre_questionnaire": "titre", "nb_questions": 2,
                                         "q_1": "texte q1", "radio_1": 1,
                                         "q_2": "qcm q2", "radio_2": 0, "nb_choix_qcm_2": 2, "qcm-2-1": "choix 1",
                                         "qcm-2-2": "choix 2"})
    assert Questionnaire.query.count() == 1
    assert Questionnaire.query.first().titre == "titre"

    assert Question.query.count() == 2
    assert Question.query.first().numero == 1
    assert Question.query.first().typeQuestion == "TEXTE"

    assert ChoixQcm.query.count() == 2
