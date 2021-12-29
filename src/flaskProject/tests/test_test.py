# Permet de tester que l'environnement de test et les liens avec la base de données de tests sont
# bien en place
from time import sleep

import pytest
from flask_sqlalchemy import SQLAlchemy


from project.database.classes import *


def test_dummy():
    # print(Utilisateur.query.count())
    assert getTrue()


def test_dummy2():
    user = Utilisateur(nom="Nom", prenom="Prenom")
    db.session.add(user)
    db.session.commit()
    print(Utilisateur.query.count())
    assert getTrue()
