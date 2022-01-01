from app import app


def test_home_get():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET)
    ALORS on verifie que la page est valide
    """
    with app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200
        assert b"Bienvenue" in response.data


def test_home_post():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (POST)
    ALORS on verifie que le code de retour est 405
    """
    with app.test_client() as test_client:
        response = test_client.post('/home')
        assert response.status_code == 405
        assert b"Bienvenue" not in response.data


def test_home_alias_get():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (GET)
    ALORS on verifie que la page est valide
    """
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Bienvenue" in response.data


def test_home_alias_post():
    """
    AVEC une application flask de test
    QUAND la page '/home' page est appellée (POST)
    ALORS on verifie que le code de retour est 405
    """
    with app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405
        assert b"Bienvenue" not in response.data
