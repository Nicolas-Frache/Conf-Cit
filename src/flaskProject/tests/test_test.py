# Permet de tester que l'environnement de test et les liens avec la base de données de tests sont
# bien en place
from time import sleep

import pytest
from flask_sqlalchemy import SQLAlchemy

from ..model.classes import *


@pytest.fixture
def getTrue(autouse=False):
    return True


def test_dummy(getTrue):
    # print(Utilisateur.query.count())
    # sleep(2)
    assert getTrue


def test_dummy2(getTrue):
    print(Utilisateur.query.count())
    assert getTrue
