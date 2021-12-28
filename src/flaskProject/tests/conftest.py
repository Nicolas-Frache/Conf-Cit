import pytest
from flask_sqlalchemy import SQLAlchemy

from .. import initdb_with_sql_file, delete_db_file
from . import create_app


# Méthode qui s'execute automatiquement au début de l'éxecution de chaque méthode de test
# Voir: https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request
#
# Réinitialise la base de données de test pour chaque classe de test
@pytest.fixture(autouse=True)
def reset_test_database():
    db = SQLAlchemy()
    db.drop_all(app=create_app())
    initdb_with_sql_file(test=True)
    print("************** RESET DB **************")


# Supprime le fichier de la base de données de test à la fin de la session de test
# Voir: https://docs.pytest.org/en/6.2.x/fixture.html#adding-finalizers-directly
@pytest.fixture(scope="session", autouse=True)
def init_and_cleanup(request):
    def clean_db_test_file():
        print("************** CLEANUP ****************")
        delete_db_file(test=True)
    request.addfinalizer(clean_db_test_file)
