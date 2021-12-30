import dateutil.utils

from project.database.classes import *


def test_utilisateur_nouveau():
    """
    AVEC un modèle Utilisateur
    QUAND on le commit on à la base
    ALORS on vérifie que l'ajout à la BD est correct
    """
    db.session.add(Utilisateur(prenom="p", nom="n"))
    db.session.commit()
    assert Utilisateur.query.count() == 1
    assert Utilisateur.query.first().nom == "n"
    assert Utilisateur.query.first().prenom == "p"


def test_utilisateur_autoincrement():
    """
       AVEC des modèles Utilisateur
       QUAND on les commit on à la base
       ALORS on vérifie que les ids ont bien été crées et sont uniques
    """
    users = []
    ids = []
    for i in range(5):
        users.append(Utilisateur(nom=i))
        db.session.add(users[-1])
    db.session.commit()
    assert Utilisateur.query.count() == 5
    for user in users:
        assert str(user.id).isnumeric()
        ids.append(user.id)
    # Test d'unicité des id
    assert all(ids.count(x) == 1 for x in ids)


def test_utilisateur_generation_aleatoire():
    """
        AVEC une base de données de test vide
        QUAND on appelle la méthode populate_with_random(n)
        ALORS on vérifie qu'on a n utilisateurs aléatoires qui ont :
            - Aux maximum 80 ans,
            - Un nombre d'années d'étude inférieur = 7,
            - Comme genre "H" ou "F",
            - Les valeurs prenom, nom et profession non nulles,
            - Un mot de passe de taille 10
            - Comme rôle "citoyen".
    """
    from project.database.populate import populate_with_random
    populate_with_random(200)
    assert Utilisateur.query.count() == 200
    anneeActuelle = dateutil.utils.today().year
    for user in Utilisateur.query.all():
        anneeNaissance = int(user.dateNaissance.split("-")[0])
        assert anneeNaissance <= anneeActuelle
        assert anneeNaissance >= anneeActuelle - 80
        assert user.nbAnneesPostBac <= 7
        assert user.sexe in ["H", "F"]
        assert not (not user.prenom and not user.nom and not user.profession)
        assert len(user.password) == 10
        assert user.role == "citoyen"
