from datetime import date, timedelta

from faker import Faker
from faker.generator import random
from flask_sqlalchemy import SQLAlchemy

from project.database.classes import Utilisateur


def populate_with_random(number=1000):
    db = SQLAlchemy()
    fake = Faker("fr_FR")
    for _ in range(number):
        utilisateur = Utilisateur(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            profession=fake.job(),
            role="citoyen",
            dateNaissance=str(fake.date_time_between(date.today() - timedelta(days=365 * 80),
                                                     date.today() - timedelta(days=365 * 18))).split(" ")[0],
            sexe=random.choice(["H", "F"]),
            nbAnneesPostBac=round(random.triangular(0, 7, 3)),
            password=fake.password(length=10, special_chars=False, upper_case=False)
        )
        db.session.add(utilisateur)
    db.session.commit()

