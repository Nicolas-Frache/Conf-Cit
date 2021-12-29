import pytest
from flask_sqlalchemy import SQLAlchemy

from project import initdb_with_sql_file, delete_db_file, db
from . import create_app, app_test


# Méthode qui s'execute automatiquement au début de l'éxecution de chaque méthode de test
# Voir: https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request
#
# Réinitialise la base de données de test pour chaque classe de test
@pytest.fixture(autouse=True)
def reset_test_database():
    from sqlalchemy import MetaData
    m = MetaData(db.engine)
    m.reflect()
    m.drop_all()
    initdb_with_sql_file(test=True)
    print("************** RESET DB **************")


# Supprime le fichier de la base de données de test à la fin de la session de test
# Voir: https://docs.pytest.org/en/6.2.x/fixture.html#adding-finalizers-directly
@pytest.fixture(scope="session", autouse=True)
def init_and_cleanup(request):
    def clean_db_test_file():
        print("************** CLEANUP ****************")
        # TODO Problème de verrou sur le fichier avec windows, à voir
        # delete_db_file(test=True)

    request.addfinalizer(clean_db_test_file)
