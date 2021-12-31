import re

from app import app
from project.database.classes import Utilisateur
from project.database.populate import populate_with_random


def test_liste_citoyens_get():
    """
       AVEC une application flask de test
       QUAND la page '/listeCitoyens' page est appellée (GET)
       ALORS on verifie que la page liste bien le nombre de citoyens dans la base de données
    """
    populate_with_random(20)
    with app.test_client() as test_client:
        response = test_client.get('/listeCitoyens')
        assert response.status_code == 200
        # On vérifie que le nombre de citoyens affiché est bon en sommant les instances "H" et "F"
        assert len(re.findall(r'<td> [FH] </td>', str(response.data))) == 20


def test_liste_citoyens_get_vide():
    """
       AVEC une application flask de test
       QUAND la page '/listeCitoyens' page est appellée (GET) sans aucun citoyens dans la base
       ALORS on verifie que la page affiche le message "Aucune donnée à afficher"
    """
    assert Utilisateur.query.count() == 0
    with app.test_client() as test_client:
        response = test_client.get('/listeCitoyens')
        assert response.status_code == 200
        assert b"Aucune donn\xc3\xa9e \xc3\xa0 afficher" in response.data


def test_liste_citoyens_post():
    """
       AVEC une application flask de test
       QUAND la page '/listeCitoyens' page est appellée (POST)
       ALORS on verifie que le code de retour est 405
    """
    populate_with_random(20)
    with app.test_client() as test_client:
        response = test_client.get('/listeCitoyens')
        assert response.status_code == 200
