from flask import request
from app import app


def test_header_get():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET)
    ALORS on vérifie que le header est valide
    """
    with app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200
        assert b"Conf-Cit" in response.data


def test_connecte():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET) avec un utilisateur connecté
    ALORS on vérifie que le header est valide
    """
    with app.test_client() as test_client:
        test_client.set_cookie('localhost', 'username', 'Mateo')
        response = test_client.get('/home')
        assert response.status_code == 200
        assert b"Connect\xc3\xa9 en tant que :" in response.data
        assert b"Visiteur anonyme" not in response.data


def test_deconecte():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET) sans utilisateur connecté
    ALORS on vérifie que le header est valide
    """
    with app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200
        assert b"Visiteur anonyme" in response.data
        assert b"Connect\xc3\xa9 en tant que :" not in response.data


def test_deconnecte_cookie():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET) et qu'un utilisateur connecté se déconnecte
    ALORS on vérifie que le cookie de connexion n'existe plus
    """
    with app.test_client() as test_client:
        response = test_client.get('/home')
        test_client.set_cookie('localhost', 'username', 'Mateo')
        assert response.status_code == 200
        response = test_client.get('/deconnexion', follow_redirects=True)
        assert response.status_code == 200
        assert 'username' not in request.cookies


def test_redirect_deconnexion():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET) et qu'un utilisateur connecté se déconnecte
    ALORS on vérifie que le cookie de connexion n'existe plus
    """
    with app.test_client() as test_client:
        response = test_client.get('/home')
        test_client.set_cookie('localhost', 'username', 'Mateo')
        assert response.status_code == 200
        response = test_client.get('/deconnexion?redirect=/listeCitoyens', follow_redirects=True)
        assert response.status_code == 200
        assert request.path == '/listeCitoyens'
